from app.extensions import ma
from app.models import Customers

#Customers schema
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customers

#init schema for serialization and deserialization
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = CustomerSchema(only=["email", "password"])