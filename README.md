# 🛒 PyShop-Ecommerce

**PyShop-Ecommerce** is a beginner-friendly e-commerce web application built using the Django web framework. It provides a clean, modular structure for managing products, enabling admin functionality, and rendering content dynamically using Django's built-in templating system. This project is ideal for anyone learning Django or looking to build real-world projects to strengthen backend and full-stack development skills.

---

## 🚀 Features

- 🔐 Admin panel to manage products (CRUD operations)
- 📦 Product catalog: name, price, stock, image support
- 🧩 Modular architecture with Django apps
- 🛠️ Built-in Django ORM and admin interface
- 🖼️ Dynamic HTML templating
- 🧑‍💻 Clean and customizable codebase

---

## 🧰 Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML (Django templating)
- **Database**: SQLite (default for Django)
- **Environment**: Virtualenv (recommended)
- **Admin Tools**: Django's built-in admin

---

## 📁 Project Structure

PyShop-Ecommerce/
│
├── pyshop/ # Main Django app
│ ├── init.py
│ ├── admin.py # Admin configurations
│ ├── apps.py
│ ├── models.py # Product model
│ ├── views.py # Renders product list
│ ├── urls.py # URL routing for the app
│ ├── migrations/ # Database migration files
│ └── templates/
│ └── products/
│ └── product_list.html
│
├── pyshop_project/ # Project-level config (manage.py sibling)
│ ├── init.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── db.sqlite3 # SQLite database
├── manage.py
├── requirements.txt
└── .gitignore


---

## ✅ Requirements

Make sure Python 3.7+ and `pip` are installed.

### Create virtual environment

```bash
python -m venv env
source env/bin/activate        # macOS/Linux
# or
.\env\Scripts\activate         # Windows

Install dependencies

pip install -r requirements.txt

⚙️ Setup Instructions
Step 1: Apply Migrations

python manage.py makemigrations
python manage.py migrate

Step 2: Create Superuser

python manage.py createsuperuser

▶️ Running the Server

python manage.py runserver

Visit the site: http://127.0.0.1:8000

Admin panel: http://127.0.0.1:8000/admin/

🛒 How to Use

    Log into the admin panel with your superuser credentials.

    Under “Products”, add new items with name, price, stock count, and an image URL.

    Visit the main page to see the product list displayed.

💡 Future Improvements

    User signup/login

    Add-to-cart and checkout functionality

    Product filtering and search

    Pagination and responsive layout

    Payment integration (e.g., Stripe)

    Full Bootstrap or Tailwind CSS frontend

    Product detail pages

🧾 License

This project is licensed under the MIT License.
🙌 Acknowledgements

This project is built as part of a learning journey in Python and Django development. Huge thanks to the Django documentation and open-source community for guidance.
🔗 Connect

Made with ❤️ by Raj Tiwari
