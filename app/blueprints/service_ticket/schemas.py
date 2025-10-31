from marshmallow import fields
from app.extensions import ma
from app.models import ServiceTicket

class serviceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested('MechanicSchema', many=True)
    customer = fields.Nested('CustomerSchema')
    class Meta:
        load_instance = False
        model = ServiceTicket
        include_fk=True
        fields = ("id", "service_date","service_desc", "customer_id", "mechanics", "customer", "vin")

class editServiceTicketSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Integer(), required=True)
    remove_mechanic_ids = fields.List(fields.Integer(), required=True)
    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids")

ServiceTicket_schema = serviceTicketSchema()
ServiceTickets_schema = serviceTicketSchema(many=True)
edit_service_ticket_schema = editServiceTicketSchema()