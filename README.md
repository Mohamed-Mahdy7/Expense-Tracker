# Expense Tracker 

A full‑stack **Expense Tracker Web Application** built with **Flask** as a **CS50x Final Project**. The app allows users to manage items, record transactions, and track income vs expenses through a clean dashboard with charts.

---
#### Video Demo:  <https://youtu.be/Gz2Ip4Sp3WA>
## Project Overview

This project was developed as the **final project for Harvard CS50x**. It demonstrates:

* Backend development with Flask
* Database modeling with SQLAlchemy
* Authentication using JWT
* CRUD operations
* Secure user session handling
* Dynamic charts with Chart.js


The goal is to help users **track expenses, manage categories, and understand spending behavior**.

---

## Tech Stack

### Backend

* **Python 3**
* **Flask**
* **Flask‑JWT‑Extended** (authentication)
* **Flask‑SQLAlchemy**
* **SQLite**

### Frontend

* **HTML5 / Jinja2**
* **Bootstrap 5**
* **JavaScript**
* **Chart.js** (Pie & Bar charts)

---

## Authentication & Security

* JWT authentication using **HttpOnly cookies**
* Access & Refresh tokens
* Logout clears tokens securely
* User‑specific data isolation

---

## Features

### Authentication

* Register
* Login
* Logout

### Categories

* Create, edit, delete categories
* Each category belongs to a user
* Prevent deletion if linked to transactions

### Transactions

* Add income & expense transactions
* Auto‑calculate totals based on category price
* Transactions linked to categories

### Dashboard

* Pie chart: **Expenses by Category**
* Bar chart: **Income vs Expenses**
* Real‑time data from backend

### Error Handling

* Custom error pages
* Friendly UI messages
* Logging for debugging

---

## Charts

Charts are rendered using **Chart.js** and populated via `data-*` attributes from Jinja templates.

* Pie Chart → Expense distribution
* Bar Chart → Income vs Expenses

---

## Project Structure

```
Expense-Tracker/
│
├── app.py
├── config.py
├── main/
│   ├── routes.py
│   ├── items.py
│   ├── transactions.py
│   └── dashboard.py
│
├── auth/
│   ├── routes.py
│   └── authentication.py
│
├── models/
│   ├── user.py
│   ├── items.py
│   └── transactions.py
│
├── templates/
│   ├── dashboard.html
│   ├── items.html
│   ├── transactions.html
│   ├── login.html
│   ├── register.html
│   └── error.html
│
├── static/
│   ├── css/
│   └── js/
│
└── README.md
```

---

## Installation & Setup

### Clone the Repository

```bash
git clone https://github.com/Mohamed-Mahdy7/Expense-Tracker.git
cd Expense-Tracker
```

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_flask_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
```

### Run the App

```bash
flask run
```

---

## Secret Keys

Generate secure keys using Python:

```python
import secrets
print(secrets.token_hex(32))
```

Use **different keys** for Flask and JWT.

---

## Known Constraints

* Categories cannot be deleted if transactions exist
* Logout requires POST request
* Each user only accesses their own data

---

## CS50 Requirements Met

* Uses Python and Flask
* Uses SQL database
* Dynamic HTML via Jinja
* Implements authentication
* Non‑trivial functionality
* Clear project purpose

---

## Author

**Mohamed Mahdy**
Backend Developer | Flask & SQLAlchemy
CS50x Final Project

---

## License

This project is for **educational purposes** as part of CS50x.

---

## Acknowledgements

* Harvard CS50x
* Flask Documentation
* Chart.js

---

> "This project reflects my journey from learning Flask basics to building a real‑world backend application."
