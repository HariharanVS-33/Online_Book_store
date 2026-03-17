from django.core.management.base import BaseCommand
from store.models import Category, Book
from decimal import Decimal


BOOKS_DATA = [
    # Fiction
    {
        'title': 'The Shadow of the Wind',
        'author': 'Carlos Ruiz Zafón',
        'description': 'A boy discovers a mysterious book by a forgotten author, and sets out to find the last remaining copies before a stranger destroys them all.',
        'price': Decimal('399.00'),
        'category': 'Fiction',
        'rating': Decimal('4.8'),
        'is_bestseller': True,
        'is_new_arrival': False,
        'pages': 487,
        'published_year': 2001,
        'isbn': '978-0143034902',
    },
    {
        'title': 'The Midnight Library',
        'author': 'Matt Haig',
        'description': 'Between life and death lies the Midnight Library — a place where Nora Seed discovers books showing every version of the life she could have lived.',
        'price': Decimal('349.00'),
        'category': 'Fiction',
        'rating': Decimal('4.7'),
        'is_bestseller': True,
        'is_new_arrival': True,
        'pages': 304,
        'published_year': 2020,
        'isbn': '978-0525559474',
    },
    {
        'title': 'Project Hail Mary',
        'author': 'Andy Weir',
        'description': "A lone astronaut must save the earth from disaster in this gripping hard sci-fi thriller. He doesn't remember his mission - or his name.",
        'price': Decimal('449.00'),
        'category': 'Fiction',
        'rating': Decimal('4.9'),
        'is_bestseller': True,
        'is_new_arrival': True,
        'pages': 476,
        'published_year': 2021,
        'isbn': '978-0593135204',
    },
    # Non-Fiction
    {
        'title': 'Atomic Habits',
        'author': 'James Clear',
        'description': 'Tiny changes, remarkable results. An easy and proven way to build good habits and break bad ones through the aggregation of marginal gains.',
        'price': Decimal('499.00'),
        'category': 'Non-Fiction',
        'rating': Decimal('4.9'),
        'is_bestseller': True,
        'is_new_arrival': False,
        'pages': 319,
        'published_year': 2018,
        'isbn': '978-0735211292',
    },
    {
        'title': 'Sapiens: A Brief History of Humankind',
        'author': 'Yuval Noah Harari',
        'description': 'From the Stone Age to Silicon Valley, an exploration of how humans came to dominate the planet and what it means for our future.',
        'price': Decimal('599.00'),
        'category': 'Non-Fiction',
        'rating': Decimal('4.8'),
        'is_bestseller': True,
        'is_new_arrival': False,
        'pages': 443,
        'published_year': 2011,
        'isbn': '978-0062316097',
    },
    {
        'title': 'The Psychology of Money',
        'author': 'Morgan Housel',
        'description': 'Timeless lessons on wealth, greed, and happiness — told through 19 short stories exploring the strange ways people think about money.',
        'price': Decimal('379.00'),
        'category': 'Non-Fiction',
        'rating': Decimal('4.7'),
        'is_bestseller': False,
        'is_new_arrival': True,
        'pages': 256,
        'published_year': 2020,
        'isbn': '978-0857197689',
    },
    # Technology
    {
        'title': 'Clean Code',
        'author': 'Robert C. Martin',
        'description': 'A handbook of agile software craftsmanship. Packed with practical advice, exercises, and case studies on writing readable, maintainable code.',
        'price': Decimal('699.00'),
        'category': 'Technology',
        'rating': Decimal('4.6'),
        'is_bestseller': True,
        'is_new_arrival': False,
        'pages': 431,
        'published_year': 2008,
        'isbn': '978-0132350884',
    },
    {
        'title': 'The Pragmatic Programmer',
        'author': 'David Thomas & Andrew Hunt',
        'description': 'Your journey to mastery. A guide for developers who want to write cleaner code, avoid common pitfalls, and grow into senior engineers.',
        'price': Decimal('749.00'),
        'category': 'Technology',
        'rating': Decimal('4.8'),
        'is_bestseller': False,
        'is_new_arrival': True,
        'pages': 352,
        'published_year': 2019,
        'isbn': '978-0135957059',
    },
    {
        'title': 'Designing Data-Intensive Applications',
        'author': 'Martin Kleppmann',
        'description': 'The definitive guide to understanding how databases, distributed systems, and data pipelines work under the hood.',
        'price': Decimal('899.00'),
        'category': 'Technology',
        'rating': Decimal('4.9'),
        'is_bestseller': True,
        'is_new_arrival': False,
        'pages': 590,
        'published_year': 2017,
        'isbn': '978-1449373320',
    },
    # Education
    {
        'title': 'Make It Stick: The Science of Successful Learning',
        'author': 'Peter C. Brown',
        'description': 'Cognitive scientists unpack the myths of learning and offer evidence-based strategies that really work for students and educators alike.',
        'price': Decimal('329.00'),
        'category': 'Education',
        'rating': Decimal('4.5'),
        'is_bestseller': False,
        'is_new_arrival': False,
        'pages': 336,
        'published_year': 2014,
        'isbn': '978-0674729018',
    },
    {
        'title': 'The Art of Learning',
        'author': 'Josh Waitzkin',
        'description': 'Chess prodigy turned martial arts champion reveals the mental principles and disciplines that allowed him to excel in any pursuit he chose.',
        'price': Decimal('349.00'),
        'category': 'Education',
        'rating': Decimal('4.6'),
        'is_bestseller': False,
        'is_new_arrival': True,
        'pages': 265,
        'published_year': 2007,
        'isbn': '978-0743277464',
    },
    {
        'title': 'A Mind for Numbers',
        'author': 'Barbara Oakley',
        'description': 'How to excel at math and science even if you flunked algebra. Backed by neuroscience, this is the learning manual nobody gave you in school.',
        'price': Decimal('399.00'),
        'category': 'Education',
        'rating': Decimal('4.7'),
        'is_bestseller': False,
        'is_new_arrival': False,
        'pages': 336,
        'published_year': 2014,
        'isbn': '978-0399165245',
    },
    # Science
    {
        'title': 'A Brief History of Time',
        'author': 'Stephen Hawking',
        'description': 'From the Big Bang to black holes, Hawking\'s landmark work on cosmology explains the nature of time and the universe in accessible language.',
        'price': Decimal('299.00'),
        'category': 'Science',
        'rating': Decimal('4.8'),
        'is_bestseller': True,
        'is_new_arrival': False,
        'is_audiobook': True,
        'pages': 212,
        'published_year': 1988,
        'isbn': '978-0553380163',
    },
    {
        'title': 'The Gene: An Intimate History',
        'author': 'Siddhartha Mukherjee',
        'description': 'A brilliant account of one of the most powerful — and potentially dangerous — ideas in the history of science: the gene.',
        'price': Decimal('549.00'),
        'category': 'Science',
        'rating': Decimal('4.7'),
        'is_bestseller': False,
        'is_new_arrival': True,
        'pages': 592,
        'published_year': 2016,
        'isbn': '978-1476733500',
    },
    {
        'title': 'The Hidden Life of Trees',
        'author': 'Peter Wohlleben',
        'description': 'A forester reveals the astonishing lives of trees — how they communicate, care for their young, and form complex social networks beneath our feet.',
        'price': Decimal('399.00'),
        'category': 'Science',
        'rating': Decimal('4.6'),
        'is_bestseller': False,
        'is_new_arrival': True,
        'is_audiobook': True,
        'pages': 288,
        'published_year': 2015,
        'isbn': '978-0778804085',
    },
]


class Command(BaseCommand):
    help = 'Seed the database with 5 categories and 15 sample books'

    CATEGORIES = [
        {'name': 'Fiction', 'icon': '📖', 'description': 'Novels, short stories, and imaginative works.'},
        {'name': 'Non-Fiction', 'icon': '🧠', 'description': 'Real stories, self-help, biographies, and more.'},
        {'name': 'Technology', 'icon': '💻', 'description': 'Programming, software, and tech innovation.'},
        {'name': 'Education', 'icon': '🎓', 'description': 'Learning, cognitive science, and academic resources.'},
        {'name': 'Science', 'icon': '🔬', 'description': 'Physics, biology, nature, and scientific discovery.'},
    ]

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding database...')

        # Create categories
        category_map = {}
        for cat_data in self.CATEGORIES:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'icon': cat_data['icon'],
                    'description': cat_data['description'],
                }
            )
            category_map[cat.name] = cat
            status = '✅ Created' if created else '⏩ Exists'
            self.stdout.write(f'  {status} category: {cat.name}')

        # Create books
        for book_data in BOOKS_DATA:
            cat_name = book_data.pop('category')
            book_data['category'] = category_map[cat_name]
            book_data.setdefault('is_audiobook', False)

            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults=book_data
            )
            status = '📚 Created' if created else '⏩ Exists'
            self.stdout.write(f'  {status} book: {book.title}')

        self.stdout.write(self.style.SUCCESS('\n🎉 Seeding complete! 5 categories & 15 books ready.'))
