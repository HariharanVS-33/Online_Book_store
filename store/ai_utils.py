import requests
import time
from django.conf import settings


def get_book_summary(title: str, author: str) -> str:
    """
    Calls Groq API to generate a brief book summary using Llama 3.3 70B.
    Returns fallback text when API key is missing or request fails.
    Retries once on 429 rate-limit errors.
    """
    api_key = settings.GROQ_API_KEY
    if not api_key:
        return (
            "🔑 AI summary is coming soon! Add your Groq API key to the .env file "
            "to unlock instant AI-powered book summaries."
        )

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful book reviewer. Write concise, engaging summaries."
            },
            {
                "role": "user",
                "content": (
                    f"Write a compelling 2-3 sentence summary of the book '{title}' by {author}. "
                    f"Focus on the main theme, what makes it unique, and why readers love it. "
                    f"Keep it under 80 words and make it engaging."
                )
            }
        ],
        "temperature": 0.7,
        "max_tokens": 150,
    }

    max_retries = 2
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            if response.status_code == 429:
                if attempt < max_retries - 1:
                    time.sleep(3)
                    continue
                return "⏳ API rate limit reached. Please wait a few seconds and try again."
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content'].strip()
        except requests.exceptions.Timeout:
            return "⏱️ The AI summary is taking longer than expected. Please try again."
        except requests.exceptions.HTTPError:
            if response.status_code == 401:
                return "❌ Invalid API key. Please check your Groq API key in the .env file."
            return f"🛑 AI service error ({response.status_code}). Please try again."
        except Exception:
            return "🤖 AI summary is temporarily unavailable. Please check back soon."
    return "🤖 AI summary is temporarily unavailable. Please check back soon."
