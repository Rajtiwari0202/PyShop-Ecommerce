# PyShop Ecommerce

PyShop is a full-stack Django e-commerce platform with a complete product purchase workflow: storefront browsing, search/filtering, authentication, cart, wishlist, reviews, checkout, order history, tracking, and PDF invoices.

It is designed to be easy for reviewers to run locally while still showing the backend fundamentals expected in a real commerce application.

## Product Highlights

- Responsive storefront with product cards, product detail pages, category filters, price filters, and search.
- Authentication-protected cart, wishlist, checkout, review, order, and invoice routes.
- Razorpay payment integration with server-side signature verification.
- Demo checkout mode when Razorpay keys are not configured, so the full flow works without external credentials.
- Django admin support for products, categories, orders, reviews, and wishlists.
- Demo catalog seeding command for portfolio screenshots and walkthroughs.
- Decimal-based money fields for safer price and total calculations.

## Tech Stack

| Area | Tools |
| --- | --- |
| Backend | Python, Django |
| Database | SQLite for local development |
| Payments | Razorpay test integration plus demo checkout fallback |
| UI | Django templates, Bootstrap 5, Bootstrap Icons |
| Documents | ReportLab PDF invoices |
| Config | python-dotenv |

## Repository Structure

```text
PyShop-Ecommerce/
|-- requirements.txt
|-- .env.example
|-- pyshop/
|   `-- core/
|       |-- manage.py
|       |-- pyshop_project/
|       `-- products/
|           |-- management/commands/seed_demo.py
|           |-- migrations/
|           |-- templates/
|           |-- admin.py
|           |-- models.py
|           |-- urls.py
|           `-- views.py
`-- README.md
```

## Local Setup

```powershell
git clone https://github.com/Rajtiwari0202/PyShop-Ecommerce.git
cd PyShop-Ecommerce
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
cd pyshop\core
py manage.py migrate
py manage.py seed_demo
py manage.py createsuperuser
py manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Environment Variables

Create `.env` from `.env.example`:

```env
SECRET_KEY=replace-with-a-secure-django-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
```

Leave the Razorpay values blank to use demo checkout mode.

## Useful Commands

```powershell
cd pyshop\core
py manage.py check
py manage.py test
py manage.py seed_demo
py manage.py runserver
```

## Demo Checkout

When `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` are blank, PyShop automatically enables demo checkout mode. Reviewers can add items to the cart, place an order, track it, and view order history without needing Razorpay credentials.

To use Razorpay test mode, set both Razorpay keys in `.env`.

## Engineering Notes

- `DecimalField` is used for money values instead of floating-point numbers.
- Cart, wishlist, checkout, order, and review routes are protected by Django authentication.
- Payment verification is handled server-side before order confirmation.
- Query access is optimized with `select_related` and `prefetch_related` in key views.
- Demo checkout mode makes the app more reviewable without weakening the real payment path.

## Portfolio Context

PyShop appears in my portfolio as a commerce/backend project focused on:

- Django fundamentals
- Authenticated purchase workflows
- Payment verification
- Admin-backed product management
- PDF invoice generation

## Author

Raj Tiwari  
GitHub: https://github.com/Rajtiwari0202  
Portfolio: https://rajtiwari0202.github.io/my_portfolio/
