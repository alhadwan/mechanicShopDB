from .schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify  
from marshmallow import ValidationError
from sqlalchemy import select, delete
from ...models import Mechanics,db
from app.extensions import limiter, cache
from . import mechanics_bp

# Create a new mechanic
@mechanics_bp.route("/", methods = ["POST"])
def create_mechanics():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # avoid duplication to the mechanic
    query = select(Mechanics).where(Mechanics.email == mechanic_data["email"])
    existing_email = db.session.execute(query).scalars().all()
    if existing_email:
        return jsonify({"error":"Email already associated with an account" }), 400
    
    new_mechanic = Mechanics(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

# Get all mechanics
@mechanics_bp.route("/", methods = ['GET'])
@cache.cached(timeout=60) # Cache this route for 60 seconds
@limiter.limit("10 per minute") # Limit to 10 requests per minute
def get_mechanics():
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Mechanics)
        mechanics = db.paginate(query, page=page, per_page=per_page)
        return mechanics_schema.jsonify(mechanics), 200
    except:
        query = select(Mechanics)
        mechanics = db.session.execute(query).scalars().all()
        return mechanics_schema.jsonify(mechanics)

#Get mechanic by Id
@mechanics_bp.route("/<int:mechanic_id>", methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({"message":"mechanic not found"})
    return mechanic_schema.jsonify(mechanic)

# Update a mechanic
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

# Delete a mechanic by ID
@mechanics_bp.route("/<int:mechanic_id>", methods = ['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({"error":"Mechanic not found"}), 404
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f'Member id: {mechanic_id}, successfully deleted.'}), 200

# Delete all mechanic
@mechanics_bp.route("/", methods=['DELETE'])
def delete_mechanics():
    db.session.execute(delete(Mechanics))
    db.session.commit()
    return jsonify({"message": "All mechanics have been deleted"}), 200

# mechanic who worked the most on the ticket
@mechanics_bp.route("/work", methods=['GET'])
def mechanic_work():
    mechanics = db.session.execute(select(Mechanics)).scalars().all()
    mechanics.sort(key=lambda mechanic: len(mechanic.service_tickets), reverse=True)
    return mechanics_schema.jsonify(mechanics), 200

# search a mechanic
@mechanics_bp.route("/search", methods=['GET'])
def search_mechanic():
    name = request.args.get('name')
    query = select(Mechanics).where(Mechanics.name.like(f"%{name}%"))
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics), 200