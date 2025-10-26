# mechanicShopDB 

Small mechanic shop DB project. It uses Flask, Flask-SQLAlchemy and stores customers, mechanics, and service tickets in a MySQLworkbench database.

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

2. Install dependencies (if `requirements.txt` exists):

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install the usual packages:

```bash
pip install Flask flask-sqlalchemy marshmallow marshmallow-sqlalchemy mysql-connector-python
```

3. Configure database credentials

The app reads DB configuration from your Flask config. Edit the config file or set an environment variable (example):

```bash
export DATABASE_URL='mysql+mysqlconnector://user:password@localhost/mechanic_db'
```

Or update the connection string in your local config file used by `create_app`.


```python
from app import create_app
app = create_app('DevelopmentConfig')
with app.app_context():
    from app.models import db
    db.create_all()
```

## Running the server

- If there is a `run.py` runner, prefer:

```bash
python run.py
```

- If the project uses a top-level `app.py` that imports the app factory, you can run:

```bash
python app.py
```

Note: Make sure your current working directory is the project root (the folder that contains `app/`).

## Endpoints

- /serviceTickets/
- /customers
- /mechanics