# 📚 PageTurn — Online Book Store

A full-stack **Django** web application for browsing and purchasing books online. Features a modern dark-themed UI, customer authentication, AI-powered book summaries using **Groq (Llama 3.3 70B)**, a cart & dummy checkout system, newsletter subscription, and a powerful admin panel.

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
| **AI Book Summary** | One-click AI-generated summaries powered by Groq API (Llama 3.3 70B) |
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
| AI | Groq API (Llama 3.3 70B Versatile) |
| Fonts | Inter, Playfair Display (Google Fonts) |
| Deployment | Gunicorn, WhiteNoise, python-decouple |

---

## 📦 Prerequisites

Make sure the following are installed on your machine before starting:

| Prerequisite | How to check | Install command (Ubuntu/Debian) |
|---|---|---|
| **Python 3.10+** | `python3 --version` | `sudo apt install python3` |
| **pip** | `pip3 --version` | `sudo apt install python3-pip` |
| **python3-venv** | *(needed for virtual environment)* | `sudo apt install python3.12-venv` |
| **Git** | `git --version` | `sudo apt install git` |

> **Windows users:** Install Python from [python.org](https://www.python.org/downloads/) (check "Add to PATH" during install). `pip` and `venv` are included automatically.

> **Groq API Key** is optional. The app works fully without it — AI summaries will show a placeholder instead.

---

## 🚀 How to Run (Step by Step)

### Step 1 — Clone the Repository

```bash
git clone https://github.com/HariharanVS-33/Online_Book_store.git
cd Online_Book_store
```

---

### Step 2 — Create & Activate Virtual Environment

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

> ✅ You should see `(venv)` at the beginning of your terminal prompt after activation.

> ⚠️ **Linux error: `ensurepip is not available`?** Run `sudo apt install python3.12-venv` first, then retry.

---

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 4 — Set Up Environment Variables

```bash
cp .env.example .env          # Linux / macOS
# copy .env.example .env      # Windows
```

Open the `.env` file in any editor and set your values:

```env
SECRET_KEY=any-random-string-for-security
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
GROQ_API_KEY=                              # Leave blank for now, or paste your key
```

> 💡 **The app runs perfectly without the Groq API key.** You can add it later anytime.

---

### Step 5 — Run Database Migrations

```bash
python3 manage.py migrate                  # Linux / macOS
# python manage.py migrate                 # Windows
```

---

### Step 6 — Load Sample Data (15 Books & 5 Categories)

```bash
python3 manage.py seed_books               # Linux / macOS
# python manage.py seed_books              # Windows
```

You should see:
```
🌱 Seeding database...
  ✅ Created category: Fiction
  ✅ Created category: Non-Fiction
  ...
  📚 Created book: Atomic Habits
  📚 Created book: Clean Code
  ...
🎉 Seeding complete! 5 categories & 15 books ready.
```

---

### Step 7 — Create Admin (Superuser) Account

```bash
python3 manage.py createsuperuser          # Linux / macOS
# python manage.py createsuperuser         # Windows
```

Enter a **username**, **email**, and **password** when prompted. This is your admin login for the admin panel.

---

### Step 8 — Start the Server

```bash
python3 manage.py runserver                # Linux / macOS
# python manage.py runserver               # Windows
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

---

### Step 9 — Open in Browser 🎉

| Page | URL |
|---|---|
| 🏠 Homepage | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) |
| 📚 Browse Books | [http://127.0.0.1:8000/books/](http://127.0.0.1:8000/books/) |
| 🔐 Customer Login | [http://127.0.0.1:8000/auth/login/](http://127.0.0.1:8000/auth/login/) |
| 📝 Customer Register | [http://127.0.0.1:8000/auth/register/](http://127.0.0.1:8000/auth/register/) |
| ⚙️ Admin Panel | [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) |

> **To stop the server**, press `Ctrl + C` in the terminal.

---

## 🔄 Running Again Later

Every time you reopen the project:

```bash
cd Online_Book_store
source venv/bin/activate          # Activate virtual environment
python3 manage.py runserver       # Start the server
```

---

## 🤖 Groq AI Setup (Optional)

The AI book summary feature uses the Groq API with the **Llama 3.3 70B** model.

### How to get your free API key:

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up (Google / GitHub login works)
3. Click **"API Keys"** in the left sidebar
4. Click **"Create API Key"** → give it any name → click **"Submit"**
5. Copy the key (starts with `gsk_...`)
6. Paste it in your `.env` file:
   ```
   GROQ_API_KEY=gsk_your-api-key-here
   ```
7. Restart the server → Go to any book detail page → Click **"✨ Generate AI Summary"**

> Without the key, everything works — AI summaries just show a friendly placeholder message instead.

---

## 🔐 Admin Panel

Login at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) with the superuser account you created in Step 7.

The admin panel gives full control over:

- 📚 **Books** — Add/edit/delete, filter by category, inline cover preview
- 📂 **Categories** — Manage book categories with icons
- 📧 **Subscribers** — View all newsletter subscriber emails
- 🛒 **Carts** — View customer carts and items
- 📦 **Orders** — Manage orders, update status (Pending → Confirmed → Shipped → Delivered)
- 👤 **User Profiles** — View customer profiles

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
│   ├── ai_utils.py              # Groq API integration (Llama 3.3 70B)
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

## 🌐 Deployment

This project is deployment-ready for platforms like **Render**, **Railway**, or **Heroku**.

Files already included:
- `Procfile` — `web: gunicorn book_store.wsgi --log-file -`
- `runtime.txt` — Python version
- `requirements.txt` — All dependencies
- **WhiteNoise** — Serves static files in production
- **python-decouple** — Reads secrets from environment variables

### Quick Deploy Steps:
1. Push to GitHub
2. Connect your repo to Render/Railway
3. Set environment variables: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `GROQ_API_KEY`
4. Deploy!

---

## 📝 Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | ✅ Yes | Django secret key (use a long random string in production) |
| `DEBUG` | ✅ Yes | `True` for development, `False` for production |
| `ALLOWED_HOSTS` | ✅ Yes | Comma-separated hostnames (e.g., `127.0.0.1,your-domain.com`) |
| `GROQ_API_KEY` | ❌ Optional | Groq API key for AI book summaries (Llama 3.3 70B) |

---

## ❓ Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'django'` | Activate the virtual environment: `source venv/bin/activate` |
| `ensurepip is not available` | Install venv: `sudo apt install python3.12-venv` |
| `Error: That port is already in use` | Kill the old process: `fuser -k 8000/tcp` and retry |
| `429 Client Error` on AI summary | Rate limit — wait 10 seconds and try again |
| `401 Unauthorized` on AI summary | Check your `GROQ_API_KEY` in `.env` is correct |

---

## 📄 License

This project is for educational purposes.

---

<p align="center">Built with Django & ❤️</p>
