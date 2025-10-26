from app.extensions import ma
from app.models import ServiceTicket

class serviceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        load_instance = False
        model = ServiceTicket
        include_fk=True


ServiceTicket_schema = serviceTicketSchema()
ServiceTickets_schema = serviceTicketSchema(many=True)