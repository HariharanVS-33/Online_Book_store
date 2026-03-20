# 📚 PageTurn — Online Book Store

A full-stack **Django** web application for browsing and purchasing books online. Features a modern dark-themed UI, customer authentication, AI-powered book summaries using **Google Gemini**, a cart & dummy checkout system, newsletter subscription, and a powerful admin panel.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Dark Premium UI** | Modern dark theme with Inter & Playfair Display fonts, glassmorphism cards, smooth hover animations |
| **Customer Auth** | Register, login, logout — customers can manage their own accounts |
| **Admin Panel** | Full Django admin with cover previews, inline order items, list filters, and editable fields |
| **Book Browsing** | Search by title/author, filter by category, view detailed book pages |
| **Categories** | Fiction 📖, Non-Fiction 🧠, Technology 💻, Education 🎓, Science 🔬 |
| **Best Sellers & New Arrivals** | Featured sections on the homepage |
| **AI Book Summary** | One-click AI-generated summaries powered by Google Gemini API |
| **Cart System** | Add/remove/update quantity — real-time subtotal calculations |
| **Dummy Checkout** | Simulated checkout flow with order confirmation |
| **Newsletter** | AJAX-based email subscription stored in the database |
| **Profile & Orders** | Customers can view their order history and status |
| **Deployment-Ready** | Configured with Gunicorn, WhiteNoise, Procfile for instant deployment |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, Django 5.x |
| Frontend | HTML5, CSS3, JavaScript, Django Templates |
| Database | SQLite (Django ORM) |
| AI | Google Gemini 1.5 Flash API |
| Fonts | Inter, Playfair Display (Google Fonts) |
| Deployment | Gunicorn, WhiteNoise, python-decouple |

---

## 📦 Prerequisites

- **Python 3.10+** installed
- **pip** (Python package manager)
- **Git** (for cloning the repo)
- **Google Gemini API Key** *(optional — the app works without it, AI summaries show a placeholder)*

---

## 🚀 How to Run (Step by Step)

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Online_Book_store.git
cd Online_Book_store
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy the example file and edit it:

```bash
cp .env.example .env
```

Open `.env` and configure:

```env
SECRET_KEY=your-random-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
GEMINI_API_KEY=your-gemini-api-key-here    # Optional
```

> **Note:** The app runs fine without a Gemini API key. AI summaries will show a friendly placeholder message instead.

### 5. Run Migrations

```bash
python3 manage.py migrate
```

### 6. Seed the Database (15 Sample Books)

```bash
python3 manage.py seed_books
```

This creates **5 categories** and **15 books** with realistic metadata.

### 7. Create a Superuser (Admin)

```bash
python3 manage.py createsuperuser
```

Follow the prompts to set your admin username and password.

### 8. Start the Development Server

```bash
python3 manage.py runserver
```

### 9. Open in Browser

| Page | URL |
|---|---|
| 🏠 Homepage | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) |
| 📚 Browse Books | [http://127.0.0.1:8000/books/](http://127.0.0.1:8000/books/) |
| 🔐 Login | [http://127.0.0.1:8000/auth/login/](http://127.0.0.1:8000/auth/login/) |
| 📝 Register | [http://127.0.0.1:8000/auth/register/](http://127.0.0.1:8000/auth/register/) |
| ⚙️ Admin Panel | [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) |

---

## 📁 Project Structure

```
Online_Book_store/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── Procfile                     # Deployment (Gunicorn)
├── runtime.txt                  # Python version for deployment
├── .env.example                 # Environment variable template
├── .gitignore                   # Git ignore rules
│
├── book_store/                  # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── store/                       # Main application
│   ├── models.py                # Category, Book, Cart, Order, Subscriber, UserProfile
│   ├── views.py                 # All views (home, books, cart, checkout, auth)
│   ├── admin.py                 # Rich admin customization
│   ├── urls.py                  # URL routing
│   ├── forms.py                 # RegisterForm, CheckoutForm, SubscribeForm
│   ├── ai_utils.py              # Google Gemini API integration
│   ├── context_processors.py    # Global cart count & categories
│   └── management/
│       └── commands/
│           └── seed_books.py    # Database seeder (15 books, 5 categories)
│
├── templates/store/             # HTML templates
│   ├── base.html                # Base layout (navbar, footer, toasts)
│   ├── home.html                # Homepage (hero, bestsellers, new arrivals)
│   ├── book_list.html           # Book grid with search & filter
│   ├── book_detail.html         # Book detail + AI summary panel
│   ├── cart.html                # Shopping cart
│   ├── checkout.html            # Checkout form
│   ├── order_confirm.html       # Order success page
│   ├── profile.html             # User profile & order history
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   └── partials/
│       └── book_card.html       # Reusable book card component
│
└── static/
    └── css/
        └── main.css             # Full dark theme design system
```

---

## 🤖 Google Gemini AI Setup

The AI book summary feature uses the Google Gemini API. To enable it:

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Create / copy your API key
3. Add it to your `.env` file:
   ```
   GEMINI_API_KEY=your-api-key-here
   ```
4. Restart the server — the "Generate AI Summary" button on every book detail page will now fetch a real AI summary

> Without the key, the app still works perfectly — it just shows a friendly placeholder message.

---

## 🔐 Admin Panel

The Django admin panel provides full control over:

- 📚 **Books** — Add/edit/delete, filter by category, inline cover preview
- 📂 **Categories** — Manage book categories with icons
- 📧 **Subscribers** — View all newsletter subscriber emails
- 🛒 **Carts** — View customer carts and items
- 📦 **Orders** — Manage orders, update status (Pending → Confirmed → Shipped → Delivered)
- 👤 **User Profiles** — View customer profiles

---

## 🌐 Deployment

This project is deployment-ready for platforms like **Render**, **Railway**, or **Heroku**.

Files included for deployment:
- `Procfile` — `web: gunicorn book_store.wsgi --log-file -`
- `runtime.txt` — Python version
- `requirements.txt` — All dependencies
- **WhiteNoise** — Serves static files in production
- **python-decouple** — Reads secrets from environment variables

### Quick Deploy Steps:
1. Push to GitHub
2. Connect your repo to Render/Railway
3. Set environment variables (`SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `GEMINI_API_KEY`)
4. Deploy!

---

## 📝 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | ✅ Yes | Django secret key (use a long random string in production) |
| `DEBUG` | ✅ Yes | `True` for development, `False` for production |
| `ALLOWED_HOSTS` | ✅ Yes | Comma-separated hostnames (e.g., `127.0.0.1,your-domain.com`) |
| `GEMINI_API_KEY` | ❌ Optional | Google Gemini API key for AI book summaries |

---

## 📄 License

This project is for educational purposes.

---

<p align="center">Built with Django & ❤️</p>
