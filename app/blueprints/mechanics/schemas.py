from app.extensions import ma
from app.models import Mechanics

#Customers schema
class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanics

#init schema for serialization and deserialization
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)