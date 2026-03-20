import time
from collections import Counter
from django.core.management.base import BaseCommand
from store.models import Book
from store.ai_utils import get_book_summary
import requests
from django.conf import settings


# Reference summaries (ground truth) for evaluation
REFERENCE_SUMMARIES = {
    'The Shadow of the Wind': (
        'A boy discovers a mysterious book in the Cemetery of Forgotten Books '
        'and sets out to uncover the truth about the author, whose works are '
        'being systematically destroyed by an enigmatic figure.'
    ),
    'The Midnight Library': (
        'Nora Seed finds herself in a library between life and death, where '
        'each book lets her experience a different version of her life she '
        'could have lived if she had made different choices.'
    ),
    'Project Hail Mary': (
        'A lone astronaut wakes up on a spaceship with amnesia and must '
        'figure out his mission to save Earth from an extinction-level threat, '
        'with the help of an unlikely alien companion.'
    ),
    'Atomic Habits': (
        'A practical guide to building good habits and breaking bad ones '
        'through small incremental changes. Focuses on the compound effect '
        'of tiny improvements and systems over goals.'
    ),
    'Sapiens: A Brief History of Humankind': (
        'A sweeping history of the human species from the Stone Age to '
        'the present, exploring how Homo sapiens came to dominate Earth '
        'through cognitive, agricultural, and scientific revolutions.'
    ),
    'The Psychology of Money': (
        'A collection of short stories exploring how people think about money, '
        'wealth, and financial decisions. Argues that financial success is more '
        'about behavior than intelligence.'
    ),
    'Clean Code': (
        'A handbook for software developers on writing readable, maintainable, '
        'and clean code. Provides principles, patterns, and practices for '
        'crafting better software through agile methodology.'
    ),
    'The Pragmatic Programmer': (
        'A guide for software developers covering best practices in coding, '
        'design, and career growth. Teaches practical approaches to becoming '
        'a more effective and efficient programmer.'
    ),
    'Designing Data-Intensive Applications': (
        'A deep dive into how modern data systems work, including databases, '
        'distributed systems, stream processing, and batch processing. '
        'Covers the architecture behind reliable and scalable applications.'
    ),
    'Make It Stick: The Science of Successful Learning': (
        'Research-backed strategies for effective learning that challenge '
        'common study methods. Shows why retrieval practice, spacing, and '
        'interleaving are more effective than rereading and highlighting.'
    ),
    'The Art of Learning': (
        'Chess prodigy Josh Waitzkin shares his journey from chess champion '
        'to martial arts world champion, revealing mental principles for '
        'mastering any skill through focus and resilience.'
    ),
    'A Mind for Numbers': (
        'A guide to excelling at math and science using techniques from '
        'neuroscience and cognitive psychology. Teaches how to overcome '
        'mental blocks and learn complex subjects effectively.'
    ),
    'A Brief History of Time': (
        'Stephen Hawking explains the nature of time, space, black holes, '
        'and the Big Bang in accessible language. Explores fundamental '
        'questions about the origin and fate of the universe.'
    ),
    'The Gene: An Intimate History': (
        'A history of genetics from Mendel to modern gene editing, exploring '
        'how genes shape identity, temperament, and disease. Examines the '
        'ethical implications of genetic manipulation.'
    ),
    'The Hidden Life of Trees': (
        'A forester reveals how trees communicate through underground networks, '
        'care for their offspring, and form complex social communities. '
        'Changes the way readers think about forests and nature.'
    ),
}


def tokenize(text):
    """Normalize and tokenize text into words."""
    text = text.lower()
    for ch in '.,!?;:()[]{}"\'-_':
        text = text.replace(ch, ' ')
    return text.split()


def get_ngrams(tokens, n):
    """Generate n-grams from token list."""
    return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]


def rouge_n(reference, hypothesis, n=1):
    """
    Compute ROUGE-N score.
    Measures n-gram overlap between reference and hypothesis.
    """
    ref_tokens = tokenize(reference)
    hyp_tokens = tokenize(hypothesis)

    ref_ngrams = Counter(get_ngrams(ref_tokens, n))
    hyp_ngrams = Counter(get_ngrams(hyp_tokens, n))

    # Count overlapping n-grams
    overlap = 0
    for ngram, count in hyp_ngrams.items():
        overlap += min(count, ref_ngrams.get(ngram, 0))

    total_ref = sum(ref_ngrams.values())
    total_hyp = sum(hyp_ngrams.values())

    precision = overlap / total_hyp if total_hyp > 0 else 0
    recall = overlap / total_ref if total_ref > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {
        'precision': round(precision * 100, 1),
        'recall': round(recall * 100, 1),
        'f1': round(f1 * 100, 1),
    }


def rouge_l(reference, hypothesis):
    """
    Compute ROUGE-L score using Longest Common Subsequence.
    Captures sentence-level structure similarity.
    """
    ref_tokens = tokenize(reference)
    hyp_tokens = tokenize(hypothesis)

    m, n = len(ref_tokens), len(hyp_tokens)
    if m == 0 or n == 0:
        return {'precision': 0, 'recall': 0, 'f1': 0}

    # LCS dynamic programming
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if ref_tokens[i-1] == hyp_tokens[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    lcs_len = dp[m][n]
    precision = lcs_len / n if n > 0 else 0
    recall = lcs_len / m if m > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {
        'precision': round(precision * 100, 1),
        'recall': round(recall * 100, 1),
        'f1': round(f1 * 100, 1),
        'lcs_length': lcs_len,
    }


def ai_relevance_score(book_title, ai_summary, reference):
    """
    Use Groq to rate how relevant & accurate the AI summary is (1-10).
    This is semantic evaluation — understands meaning, not just keywords.
    """
    api_key = settings.GROQ_API_KEY
    if not api_key:
        return None

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert evaluator. Rate how accurately an AI-generated "
                    "book summary captures the key themes and content of a book. "
                    "Reply with ONLY a single number from 1 to 10. Nothing else."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Book: {book_title}\n\n"
                    f"Reference summary: {reference}\n\n"
                    f"AI-generated summary: {ai_summary}\n\n"
                    f"Rate the AI summary's accuracy from 1 (completely wrong) to 10 (perfect). "
                    f"Reply with ONLY the number."
                )
            }
        ],
        "temperature": 0.1,
        "max_tokens": 5,
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        resp.raise_for_status()
        score_text = resp.json()['choices'][0]['message']['content'].strip()
        score = int(''.join(c for c in score_text if c.isdigit())[:2])
        return min(max(score, 1), 10)
    except Exception:
        return None


class Command(BaseCommand):
    help = 'Evaluate AI summary accuracy using ROUGE-1, ROUGE-L, and AI Semantic Scoring'

    def handle(self, *args, **options):
        books = Book.objects.all()
        results = []
        evaluated = 0
        skipped = 0

        self.stdout.write('\n' + '=' * 75)
        self.stdout.write('  📊 AI BOOK SUMMARY — ACCURACY EVALUATION')
        self.stdout.write('  Model        : Llama 3.3 70B via Groq API')
        self.stdout.write('  Metrics      : ROUGE-1 | ROUGE-L | AI Semantic Score')
        self.stdout.write('  Books        : 15')
        self.stdout.write('=' * 75 + '\n')

        totals = {'rouge1': 0, 'rougeL': 0, 'semantic': 0, 'semantic_count': 0}

        for book in books:
            if book.title not in REFERENCE_SUMMARIES:
                skipped += 1
                continue

            self.stdout.write(f'  📚 {book.title} — {book.author}')
            self.stdout.write(f'     Generating AI summary...')

            ai_summary = get_book_summary(book.title, book.author)

            if ai_summary.startswith(('🔑', '⏳', '⏱️', '❌', '🛑', '🤖')):
                self.stdout.write(self.style.WARNING(f'     ⚠️  Skipped: {ai_summary[:60]}'))
                skipped += 1
                time.sleep(2)
                continue

            ref = REFERENCE_SUMMARIES[book.title]

            # ROUGE-1 (unigram overlap)
            r1 = rouge_n(ref, ai_summary, n=1)
            # ROUGE-L (longest common subsequence)
            rl = rouge_l(ref, ai_summary)
            # AI semantic evaluation
            sem = ai_relevance_score(book.title, ai_summary, ref)

            self.stdout.write(f'     AI Output : {ai_summary[:90]}...')
            self.stdout.write(f'     ROUGE-1   : P={r1["precision"]}% R={r1["recall"]}% F1={r1["f1"]}%')
            self.stdout.write(f'     ROUGE-L   : P={rl["precision"]}% R={rl["recall"]}% F1={rl["f1"]}%')
            if sem is not None:
                self.stdout.write(f'     Semantic  : {sem}/10 ({sem * 10}%)')
            self.stdout.write('')

            totals['rouge1'] += r1['f1']
            totals['rougeL'] += rl['f1']
            if sem is not None:
                totals['semantic'] += sem
                totals['semantic_count'] += 1

            results.append({
                'title': book.title,
                'rouge1_f1': r1['f1'],
                'rougeL_f1': rl['f1'],
                'semantic': sem,
            })

            evaluated += 1
            time.sleep(1.5)

        # ── RESULTS ──
        self.stdout.write('=' * 75)
        self.stdout.write('  📈 OVERALL RESULTS')
        self.stdout.write('=' * 75)

        if evaluated > 0:
            avg_r1 = round(totals['rouge1'] / evaluated, 1)
            avg_rl = round(totals['rougeL'] / evaluated, 1)
            avg_sem = round(totals['semantic'] / totals['semantic_count'], 1) if totals['semantic_count'] > 0 else 0
            avg_sem_pct = round(avg_sem * 10, 1)

            self.stdout.write(f'\n  Books Evaluated    : {evaluated}')
            self.stdout.write(f'  Books Skipped      : {skipped}')
            self.stdout.write(f'  ─────────────────────────────────────────')
            self.stdout.write(f'  Avg ROUGE-1 F1     : {avg_r1}%')
            self.stdout.write(f'  Avg ROUGE-L F1     : {avg_rl}%')
            self.stdout.write(self.style.SUCCESS(f'  Avg Semantic Score : {avg_sem}/10 ({avg_sem_pct}%)  ← AI Accuracy'))
            self.stdout.write(f'  ─────────────────────────────────────────\n')

            # Per-book table
            self.stdout.write(f'  {"Book":<43} {"ROUGE-1":>8} {"ROUGE-L":>8} {"Semantic":>9}')
            self.stdout.write(f'  {"─" * 43} {"─" * 8} {"─" * 8} {"─" * 9}')
            for r in sorted(results, key=lambda x: (x['semantic'] or 0, x['rougeL_f1']), reverse=True):
                title = r['title'][:41]
                sem_str = f'{r["semantic"]}/10' if r['semantic'] else '  N/A'
                self.stdout.write(f'  {title:<43} {r["rouge1_f1"]:>7}% {r["rougeL_f1"]:>7}% {sem_str:>9}')

            self.stdout.write(f'\n  ─────────────────────────────────────────')
            self.stdout.write(f'  ℹ️  Scoring Methods:')
            self.stdout.write(f'  • ROUGE-1  = Unigram (word) overlap F1 score')
            self.stdout.write(f'  • ROUGE-L  = Longest Common Subsequence F1 score')
            self.stdout.write(f'  • Semantic = AI-judged relevance (1-10 scale, most meaningful)')
            self.stdout.write(f'\n  💡 ROUGE scores of 20-40% are normal for abstractive summarization.')
            self.stdout.write(f'     Semantic scores of 7-9/10 indicate high-quality summaries.')
        else:
            self.stdout.write(self.style.ERROR('\n  ❌ No books evaluated. Check your GROQ_API_KEY in .env'))

        self.stdout.write('\n' + '=' * 75 + '\n')
