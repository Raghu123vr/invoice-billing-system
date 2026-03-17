# Billing System (Django)

This is a simple billing system developed using Django.
It allows adding products, generating bills, viewing previous purchases, and sending invoices via email.

---

## Features

- Add multiple products in a single bill
- Automatic tax calculation
- Cash denomination handling
- Previous purchase history
- Email invoice sending
- Simple UI (focus on Model & View logic)

---

## Requirements

- Python 3.10+
- pip

---

## Installation Steps

### 1. Clone the repository

git clone https://github.com/Raghu123vr/invoice-billing-system
cd invoice-billing-system
cd billing_project


### 2. Create virtual environment



python -m venv myvenv
myvenv\Scripts\activate




### 3. Install dependencies

pip install -r requirements.txt


### 4. Apply migrations

python manage.py migrate


### 5. Run server

python manage.py runserver


### 6. Open in browser

http://127.0.0.1:8000/bill/

---

## Email Configuration

To enable invoice email:

Go to settings.py and update:

EMAIL_HOST_USER = your_gmail
EMAIL_HOST_PASSWORD = your_app_password

---

## Notes

- Focus is on backend logic (Model & View)
- Minimal CSS used
- SQLite database used

---

## Developed By

Raghu V R