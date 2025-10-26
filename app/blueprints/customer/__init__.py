from flask import Blueprint

customers_bp = Blueprint('customers_bp', __name__) # Blueprint for customer routes how? - and what is the __name__ for? The __name__ is the name of the current module, which is used by Flask to determine the location of templates and static files.

from . import routes