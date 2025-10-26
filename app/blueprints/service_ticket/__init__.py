from flask import Blueprint
serviceTicket_bp = Blueprint("service_ticket_bp", __name__)
from . import routes

