# 🛍 PyShop — Modern Django E-Commerce Platform

PyShop is a full-stack modern e-commerce web application built using Django.  
It includes authentication, cart system, Razorpay payment integration, wishlist, reviews, invoices, order tracking, and a responsive modern UI.

---

# 🚀 Features

## 🔐 Authentication System
- User Signup
- User Login / Logout
- Protected routes using Django authentication

## 🛒 Shopping Features
- Add to Cart
- Remove from Cart
- Increase / Decrease Quantity
- Wishlist System
- Buy Now functionality

## 💳 Payment Gateway
- Razorpay Integration
- Secure Payment Verification
- UPI / Card / Net Banking support
- Payment Success Flow

## 📦 Order Management
- Order History
- Track Orders
- Invoice Download System
- Real-time Order Status

## ⭐ Product Reviews
- Product Ratings
- Customer Reviews
- Average Rating System

## 🔍 Product Features
- Product Search
- Category Filtering
- Price Filtering
- Related Products

## 🎨 Modern UI
- Responsive Bootstrap 5 Design
- Toast Notifications
- Beautiful Product Cards
- Mobile-Friendly Layout
- Smooth Hover Effects

---

# 🛠 Tech Stack

| Technology | Usage |
|------------|-------|
| Python | Backend |
| Django | Web Framework |
| SQLite | Database |
| Razorpay | Payment Gateway |
| Bootstrap 5 | Frontend Styling |
| HTML/CSS | Frontend |
| JavaScript | Dynamic Features |

---

# 📂 Project Structure

```bash
pyshop/
│
├── core/
│   ├── products/
│   │   ├── migrations/
│   │   ├── templates/
│   │   │   └── products/
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── context_processors.py
│   │
│   ├── core/
│   └── manage.py
│
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/PyShop-Ecommerce.git
```

## 2️⃣ Navigate to Project

```bash
cd PyShop-Ecommerce
```

## 3️⃣ Create Virtual Environment

```bash
python -m venv venv
```

## 4️⃣ Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

# 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Setup Environment Variables

Create a `.env` file:

```env
RAZORPAY_KEY_ID=your_key
RAZORPAY_KEY_SECRET=your_secret
SECRET_KEY=your_django_secret
DEBUG=True
```

---

# 🗄 Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# 👤 Create Superuser

```bash
python manage.py createsuperuser
```

---

# ▶ Run Server

```bash
python manage.py runserver
```

Visit:

```bash
http://127.0.0.1:8000/
```

---

# 💳 Razorpay Test Payment

Use Razorpay Test Mode:

### Test Card

```text
Card Number: 4111 1111 1111 1111
Expiry: Any future date
CVV: Any 3 digits
OTP: 1234
```

### Test UPI

```text
success@razorpay
```

---

# 📸 Screenshots

## 🏠 Homepage
- Product Listing
- Filters
- Search System

## 🛒 Cart Page
- Quantity Controls
- Dynamic Total

## 💳 Payment Page
- Razorpay Checkout
- UPI Payments

## 📦 Orders
- Order Tracking
- Invoice Download

---

# 🔥 Future Improvements

- PostgreSQL Integration
- Docker Deployment
- AI Product Recommendations
- Email Invoice System
- REST API
- React Frontend
- Admin Analytics Dashboard
- Redis Caching
- Coupon System

---

# 📚 What I Learned

- Django Authentication
- Payment Gateway Integration
- Database Relationships
- Secure Payment Verification
- Dynamic UI Rendering
- E-Commerce Workflows
- Full Stack Development

---

# 👨‍💻 Author

## Raj Tiwari

Built with ❤️ using Django

GitHub:
https://github.com/YOUR_USERNAME

---

# ⭐ Support

If you like this project:

- Star this repository ⭐
- Fork it 🍴
- Share it 🚀

---

# 📄 License

This project is for educational purposes.