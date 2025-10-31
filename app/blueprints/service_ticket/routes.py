from .schemas import ServiceTicket_schema, ServiceTickets_schema, edit_service_ticket_schema
from app.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select, delete
from ...models import ServiceTicket, Customers, Mechanics, db
from . import serviceTicket_bp

# Create a new service ticket
@serviceTicket_bp.route("/", methods=["POST"])
def create_serviceTickets():
    try:
        serviceTicket_data = ServiceTicket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    customer = db.session.get(Customers, serviceTicket_data["customer_id"])
    if not customer:
        return jsonify({"error":"customer_id not found"}), 400
    # query = select(ServiceTicket).where(ServiceTicket.vin == serviceTicket_data['vin'])
    # # existing_vin = db.session.execute(query).scalars().all()
    # # if existing_vin:
    # #     return jsonify({"error": "service ticket already associated with an account."}), 400
    new_serviceTicket = ServiceTicket(**serviceTicket_data)
    db.session.add(new_serviceTicket)
    db.session.commit()
    return ServiceTicket_schema.jsonify(new_serviceTicket), 201

# Get all service tickets
@serviceTicket_bp.route("/", methods=['GET'])
def get_serviceTickets():
    query = select(ServiceTicket)
    serviceTickets = db.session.execute(query).scalars().all()
    return ServiceTickets_schema.jsonify(serviceTickets)

# Get a service ticket by ID
@serviceTicket_bp.route("/<int:ticket_id>", methods=['GET'])
def get_serviceTicket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"message":"ticket not found"})
    return ServiceTicket_schema.jsonify(ticket)

# assign a mechanic to a service ticket
@serviceTicket_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not ticket or not mechanic:
        return jsonify({"error":"ticket or mechanic not found"})

    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()
    return jsonify({
       "message": "successfully assigned mechanic to service ticket",
       "ticket": ServiceTicket_schema.dump(ticket),
       "mechanics": mechanics_schema.dump(ticket.mechanics)
    }),200

# remove a mechanic from a service ticket
@serviceTicket_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id) # get the service ticket instance by its ID
    mechanic = db.session.get(Mechanics, mechanic_id) # get the mechanic instance by its ID
    if not ticket or not mechanic:
        return jsonify({"error":"ticket or mechanic not found"})
   # Remove the mechanic from the service ticket's mechanics list if they are assigned
    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()
    return jsonify({
       "message": "successfully assigned mechanic to service ticket",
       "ticket": ServiceTicket_schema.dump(ticket),
       "mechanics": mechanics_schema.dump(ticket.mechanics)
    }),200

# Update a service ticket
@serviceTicket_bp.route("/<int:ticket_id>", methods=['PUT'])
def update_serviceTicket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"message":"ticket not found"})
    try:
        ticket_data = edit_service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for mechanic_id in ticket_data['add_mechanic_ids']:
        mechanic = db.session.get(Mechanics, mechanic_id)
        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)

    for mechanic_id in ticket_data['remove_mechanic_ids']:
        mechanic = db.session.get(Mechanics, mechanic_id)
        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)
            
    db.session.commit()
    return ServiceTicket_schema.jsonify(ticket), 200

# Delete a service ticket by ID
@serviceTicket_bp.route("/<int:ticket_id>", methods=['DELETE'])
def delete_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"message":"ticket not found"})
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f'Member id: {ticket_id}, successfully deleted.'}), 200

# Delete all service tickets
@serviceTicket_bp.route("/", methods=['DELETE'])
def delete_tickets():
    db.session.execute(delete(ServiceTicket))
    db.session.commit()
    return jsonify({"message": "All tickets have been deleted"}), 200





