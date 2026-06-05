# PyShop - Premium Django E-Commerce Platform

PyShop is a full-stack Django commerce application with a polished storefront, authentication, cart management, wishlist, reviews, checkout, invoices, and order tracking. It is designed to be easy to run locally and strong enough to discuss in interviews as a complete product workflow.

## Highlights

- Premium responsive storefront with search, category filters, price filters, and product detail pages.
- Authentication-protected cart, wishlist, checkout, reviews, orders, tracking, and invoices.
- Razorpay integration with server-side signature verification.
- Demo checkout mode when Razorpay keys are not configured, so reviewers can complete the full purchase flow locally.
- Decimal-based money fields for safer totals.
- Django admin support for products, categories, orders, reviews, and wishlists.
- Demo catalog seeding command for screenshots and portfolio walkthroughs.

## Tech Stack

| Layer | Tools |
| --- | --- |
| Backend | Python, Django |
| Database | SQLite for local development |
| Payments | Razorpay test integration plus demo mode |
| UI | Django templates, Bootstrap 5, Bootstrap Icons |
| Documents | ReportLab PDF invoices |
| Config | python-dotenv |

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

## Demo Checkout

If `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` are blank, the app automatically enables demo checkout mode. This lets anyone add items to cart, confirm payment, generate an order, track it, and view the order history without external credentials.

To use Razorpay test mode, set both keys in `.env`.

## Useful Commands

```powershell
cd pyshop\core
py manage.py check
py manage.py test
py manage.py seed_demo
py manage.py runserver
```

## Resume Bullets

- Built a Django e-commerce platform with product discovery, category and price filtering, authenticated cart, wishlist, reviews, checkout, order tracking, and PDF invoice generation.
- Integrated Razorpay payment verification with a local demo checkout fallback to make the full purchase workflow reviewable without external credentials.
- Improved production readiness by moving secrets to environment variables, using Decimal money fields, adding admin tooling, and optimizing query access with `select_related` and `prefetch_related`.
- Designed a premium responsive storefront using Django templates, Bootstrap 5, and reusable UI patterns for a polished portfolio presentation.

## Interview Talking Points

- Why money values use `DecimalField` instead of float.
- How Razorpay signature verification protects the payment flow.
- How demo checkout mode improves project reviewability.
- How Django auth decorators protect cart, checkout, wishlist, orders, and reviews.
- How the order lifecycle is represented through `Order` and `OrderItem`.

## Project Structure

```text
PyShop-Ecommerce/
├── requirements.txt
├── .env.example
├── pyshop/
│   └── core/
│       ├── manage.py
│       ├── pyshop_project/
│       └── products/
│           ├── management/commands/seed_demo.py
│           ├── migrations/
│           ├── templates/
│           ├── admin.py
│           ├── models.py
│           ├── urls.py
│           └── views.py
```

## Author

Raj Tiwari  
GitHub: https://github.com/Rajtiwari0202
