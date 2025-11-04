from flask import Flask
from dotenv import load_dotenv
from .extensions import ma, limiter, cache
from .models import db
from .blueprints.customer import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.Inventory import inventory_bp
from .blueprints.service_ticket import serviceTicket_bp
from flask_swagger_ui import get_swaggerui_blueprint
import os

load_dotenv()

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Mechanic Shop API"
    }
)


def create_app(config_name="DevelopmentConfig"):
    app = Flask(__name__)

    if config_name.startswith("config."):
        app.config.from_object(config_name)
    else:
        app.config.from_object(f"config.{config_name}")

    # initialize extensions
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    # register blueprints
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(serviceTicket_bp, url_prefix="/serviceTickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app