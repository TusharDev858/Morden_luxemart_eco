# 🛍️ LuxeMart – Premium Django E-Commerce

A complete, production-ready e-commerce platform built with Django, featuring a modern premium UI/UX with dark mode, animations, full payment integration, and a powerful admin panel.

---

## ✨ Features

### 🛒 E-Commerce
- Product catalog with search, filtering, sorting, pagination
- Product detail with image gallery & zoom, variants, related products
- Shopping cart (session + user-based, with merge on login)
- Wishlist system
- Coupon/discount code system
- **Stripe** (card payments) + **PayPal** integration
- Cash on Delivery option
- Order tracking with visual step progress bar
- Order history and management

### 👤 User System
- Custom user model (email-based auth)
- Registration, Login, Logout
- Password reset via email
- User profile with avatar upload
- Saved shipping addresses (multiple)
- Account dashboard with stats
- Order history

### 🎨 UI/UX
- Animated hero slider
- Dark / Light mode toggle (persisted)
- Glassmorphism effects
- Smooth scroll animations (IntersectionObserver)
- Responsive: mobile, tablet, laptop, 4K
- Toast notification system
- AI-style chatbot UI
- Animated product cards with hover effects
- Product image zoom on hover

### 🔒 Admin Panel
- Full Django admin with inline image upload
- Superuser dashboard
- Product, Category, Brand, Banner, Order, User, Review, Coupon management
- Inventory tracking
- Order status management

---

## 🚀 Quick Start (Local)

```bash
# 1. Clone and enter project
git clone <repo-url>
cd ecommerce

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your keys

# 5. Run migrations
python manage.py migrate

# 6. Seed demo data (products, categories, users, reviews)
python manage.py seed_data

# 7. Start development server
python manage.py runserver
```

Open http://127.0.0.1:8000

**Admin Panel:** http://127.0.0.1:8000/admin  
**Login:** `admin@luxemart.com` / `Admin@1234`

---

## 🐳 Docker Deployment

```bash
# Copy and configure env
cp .env.example .env
# Edit .env (set SECRET_KEY, Stripe keys, etc.)

# Build and run
docker-compose up --build -d

# View logs
docker-compose logs -f web
```

Open http://localhost

---

## ⚙️ Environment Variables (`.env`)

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for development, `False` for production |
| `DATABASE_URL` | PostgreSQL connection string |
| `STRIPE_PUBLIC_KEY` | Stripe publishable key |
| `STRIPE_SECRET_KEY` | Stripe secret key |
| `PAYPAL_CLIENT_ID` | PayPal client ID |
| `EMAIL_HOST_USER` | SMTP email address |
| `EMAIL_HOST_PASSWORD` | SMTP password / app password |

---

## 📁 Project Structure

```
ecommerce/
├── ecommerce/          # Django project config
│   ├── settings.py
│   └── urls.py
├── store/              # Products, Categories, Banners
├── users/              # Custom user, auth, profile
├── cart/               # Session-based cart
├── wishlist/           # User wishlist
├── orders/             # Checkout, payments, tracking
├── reviews/            # Product reviews & ratings
├── contact/            # Contact form, FAQ
├── static/
│   ├── css/main.css    # Premium design system
│   └── js/main.js      # All interactions
├── templates/          # All HTML templates
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
└── requirements.txt
```

---

## 💳 Payment Setup

### Stripe
1. Create account at [stripe.com](https://stripe.com)
2. Get test keys from Dashboard → Developers → API keys
3. Add to `.env`: `STRIPE_PUBLIC_KEY` and `STRIPE_SECRET_KEY`

### PayPal
1. Create app at [developer.paypal.com](https://developer.paypal.com)
2. Get sandbox credentials
3. Add to `.env`: `PAYPAL_CLIENT_ID` and `PAYPAL_CLIENT_SECRET`

---

## 🎨 Demo Accounts

After running `python manage.py seed_data`:

| Role | Email | Password |
|---|---|---|
| Admin | admin@luxemart.com | Admin@1234 |
| User 1 | user1@luxemart.com | User@1234 |
| User 2 | user2@luxemart.com | User@1234 |

**Demo Coupons:** `WELCOME10` (10% off) · `LUXE20` (20% off) · `FLAT25` ($25 off)

---

## 📱 Responsive Breakpoints

| Device | Width |
|---|---|
| Mobile | < 480px |
| Tablet | 480px – 768px |
| Laptop | 768px – 1024px |
| Desktop | 1024px – 1400px |
| 4K | > 1400px |

---

## 🛡️ Security

- CSRF protection on all forms
- Honeypot anti-spam on contact form
- Secure session handling
- Password hashing (Django default)
- XSS protection headers
- SQL injection prevention (Django ORM)
- SSL/HTTPS ready (configure in production)

---

Built with ❤️ using Django 4.2 · Bootstrap 5 · Stripe · PayPal
