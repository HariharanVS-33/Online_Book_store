import requests
from django.conf import settings


def get_book_summary(title: str, author: str) -> str:
    """
    Calls Google Gemini API to generate a brief book summary.
    Returns fallback text when API key is missing or request fails.
    """
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        return (
            "🔑 AI summary is coming soon! Add your Gemini API key to the .env file "
            "to unlock instant AI-powered book summaries."
        )

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-1.5-flash:generateContent?key={api_key}"
    )

    prompt = (
        f"Write a compelling 2-3 sentence summary of the book '{title}' by {author}. "
        f"Focus on the main theme, what makes it unique, and why readers love it. "
        f"Keep it under 80 words and make it engaging."
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 150,
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text'].strip()
    except requests.exceptions.Timeout:
        return "⏱️ The AI summary is taking longer than expected. Please try again in a moment."
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            return "❌ Invalid API key. Please check your Gemini API key in the .env file."
        return f"🛑 AI service error: {str(e)}"
    except Exception:
        return "🤖 AI summary is temporarily unavailable. Please check back soon."
