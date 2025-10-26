from .schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify  
from marshmallow import ValidationError
from sqlalchemy import select
from ...models import Mechanics,db
from . import mechanics_bp

@mechanics_bp.route("/", methods = ["POST"])
def create_mechanics():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Mechanics).where(Mechanics.email == mechanic_data["email"])
    existing_email = db.session.execute(query).scalars().all()
    if existing_email:
        return jsonify({"error":"Email already associated with an account" }), 400
    
    new_mechanic = Mechanics(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

@mechanics_bp.route("/", methods = ['GET'])
def get_mechanic():
    query = select(Mechanics)
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics)

@mechanics_bp.route("/<int:mechanic_id>", methods = ['PUT'])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    
    if not mechanic:
        return jsonify({"error":"mechanic not found"}), 404
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key,value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()

    return mechanic_schema.jsonify(mechanic), 200

@mechanics_bp.route("/<int:mechanic_id>", methods = ['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({"error":"Mechanic not found"}), 404
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f'Member id: {mechanic_id}, successfully deleted.'}), 200
