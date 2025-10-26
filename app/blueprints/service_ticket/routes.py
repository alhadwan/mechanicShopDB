from .schemas import ServiceTicket_schema, ServiceTickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from ...models import ServiceTicket, Customers, Mechanics, db
from . import serviceTicket_bp


@serviceTicket_bp.route("/", methods=["POST"])
def create_serviceTickets():
    try:
        serviceTicket_data = ServiceTicket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    customer = db.session.get(Customers, serviceTicket_data["customer_id"])
    if not customer:
        return jsonify({"error":"customer_id not found"}), 400
    query = select(ServiceTicket).where(ServiceTicket.vin == serviceTicket_data['vin'])
    # existing_vin = db.session.execute(query).scalars().all()
    # if existing_vin:
    #     return jsonify({"error": "service ticket already associated with an account."}), 400
    new_serviceTicket = ServiceTicket(**serviceTicket_data)
    db.session.add(new_serviceTicket)
    db.session.commit()
    return ServiceTicket_schema.jsonify(new_serviceTicket), 201

@serviceTicket_bp.route("/", methods=['GET'])
def get_serviceTickets():
    query = select(ServiceTicket)
    serviceTickets = db.session.execute(query).scalars().all()
    return ServiceTickets_schema.jsonify(serviceTickets)

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
        "message":f'ticket id: {ticket_id}, successfully assign to mechanic id: {mechanic_id}.'
    }),200

@serviceTicket_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not ticket or not mechanic:
        return jsonify({"error":"ticket or mechanic not found"})

    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()
    return jsonify({
        "message":f'ticket id: {ticket_id}, successfully removed from mechanic id: {mechanic_id}.'
    }),200





