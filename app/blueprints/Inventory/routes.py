from .schemas import inventory_schema, inventories_schema
from flask import request, jsonify  
from marshmallow import ValidationError
from sqlalchemy import select, delete
from ...models import Inventory,db
from app.extensions import limiter, cache
from . import inventory_bp
from app.utils.utils import encode_token, token_required

# Create an inventory
@inventory_bp.route("/", methods=['POST'])
def create_inventory():
    try:
        inventory  = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_inventory = Inventory(**inventory)
    db.session.add(new_inventory)
    db.session.commit()
    return inventory_schema.dump(new_inventory), 201

# Get all the inventories
@inventory_bp.route("/", methods=['GET'])
def get_inventories():
    inventories = db.session.execute(select(Inventory)).scalars().all()
    return inventories_schema.dump(inventories), 200

#update an inventory
@inventory_bp.route("/<int:inventory_id>", methods=['PUT'])
def update_inventory(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)
    if not inventory:
        return jsonify({"message":"inventory not found"})

    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in inventory_data.items():
        setattr(inventory, key, value)
    db.session.commit()
    return inventory_schema.dump(inventory), 200

# Delete all inventories
@inventory_bp.route("/", methods=['DELETE'])
def delete_inventory():
    db.session.execute(delete(Inventory))
    db.session.commit()
    return jsonify({"message": "All inventories have been deleted"}), 200