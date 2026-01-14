# Django E-Commerce

A fully functional e-commerce web application built with Django.

## Features

- User authentication and authorization
- Product catalog with categories
- Shopping cart functionality
- Order management
- Payment integration
- Admin dashboard
- Responsive design

## Technologies Used

- Python
- Django
- SQLite/PostgreSQL
- HTML/CSS
- JavaScript
- Bootstrap

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rizwansakhawat/Django-E_Commerce.git
cd Django-E_Commerce
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Start the development server:
```bash
python manage.py runserver
```

7. Visit `http://localhost:8000` in your browser

## Usage

- Access the admin panel at `/admin`
- Browse products and add them to cart
- Proceed to checkout and complete orders

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.