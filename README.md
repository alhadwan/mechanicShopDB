# mechanicShopDB

mechanic shop DB project. It uses Flask, Flask-SQLAlchemy and stores customers, mechanics, inventories and service tickets in a MySQLworkbench database.

## Demo
Live Demo: https://mechanicshopdb.onrender.com/api/docs/

## Tech used

- Language: Python
- Framework: Flask
- ORM: Flask-SQLAlchemy with SQLAlchemy 2 DeclarativeBase
- Serialization/deserialization: marshmallow / flask-marshmallow
- Database: MySQL (mysql-connector)

## Install & setup

1. Create and activate a venv (macOS / zsh):

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Environment variables

Use the .env example as a reference to create a `.env` file in the project root.

```bash
# Example .env
FLASK_ENV=development
FLASK_APP=run.py
DATABASE_USER=myuser
DATABASE_PASSWORD=mypassword
DATABASE_HOST=127.0.0.1
DATABASE_NAME=mechanic_db
# Or provide a full connection string
SQLALCHEMY_DATABASE_URI=mysql+mysqlconnector://myuser:mypassword@127.0.0.1/mechanic_db
```

4. Create the database (example using MySQL):

```bash
# create database from MySQL shell or a client
mysql -u root -p
CREATE DATABASE mechanic_db;
```

5. Create tables (app context)

```bash
python -c "from app import create_app; app = create_app();
with app.app_context():
    from app.models import db
    db.create_all()"
```

## Running the server

```bash
python app.py
```

## Blueprint / endpoint summary

- Inventory: CRUD endpoints under `/inventory`
- Customers: CRUD endpoints under `/customers`
- Mechanics: CRUD endpoints under `/mechanics`
- Service tickets: CRUD endpoints under `/service_tickets`
