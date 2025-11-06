from .schemas import customer_schema, customers_schema, login_schema
from flask import request, jsonify  
from marshmallow import ValidationError
from sqlalchemy import select, delete
from ...models import Customers,db
from . import customers_bp
from app.extensions import limiter, cache
from app.utils.utils import encode_token, token_required

# Customer Login
@customers_bp.route("/login", methods = ["POST"])
def login_customer():
    try:
        customer_credentials = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customers).where(Customers.email == customer_credentials['email']) #Checking our db for a member with this email
    customer = db.session.execute(query).scalars().first()
    if customer and customer.password == customer_credentials['password']:
        auth_token = encode_token(customer.id)
        response = {
            "status": "success",
            "message": "Successfully Logged In",
            "auth_token": auth_token
        }
        return jsonify(response), 200
    else:
        return jsonify({"error": "Invalid email or password."}), 401

# Create a new customer
@customers_bp.route("/", methods = ["POST"])
@limiter.limit("10 per minute")  # Rate limiting: max 10 requests per minute
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customers).where(Customers.email == customer_data['email']) #Checking our db for a member with this email
    existing_member = db.session.execute(query).scalars().all()
    if existing_member:
        return jsonify({"error": "Email already associated with an account."}), 400
        

    new_customer = Customers(**customer_data) # ex Customers(name=customer_data['name'], ...)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

# Get all customers
@customers_bp.route("/", methods = ['GET'])
# @cache.cached(timeout=60)  # Cache this route for 60 seconds
def get_customers():
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Customers)
        customers = db.paginate(query, page=page, per_page=per_page)
        return customers_schema.jsonify(customers), 200
    except:
        query = select(Customers)
        customers = db.session.execute(query).scalars().all()
        return customers_schema.jsonify(customers)

#Get customer by Id
@customers_bp.route("/<int:customer_id>", methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customers, customer_id)
    if not customer:
        return jsonify({"message":"customer not found"})
    return customer_schema.dump(customer)


# Update a customer
@customers_bp.route("/", methods=['PUT'])
@token_required
def update_customer(customer_id):
    customer = db.session.get(Customers, customer_id)

    if not customer:
        return jsonify({"error": "customer not found."}), 404
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in customer_data.items():
        #setting the attributes of the customer object to the new values from customer_data
        setattr(customer, key, value) 

    db.session.commit()
    return customer_schema.jsonify(customer), 200

# Delete a customer by ID
@customers_bp.route("/", methods=['DELETE'])
@token_required
def delete_customer(customer_id): #id received from token
    customer = db.session.get(Customers, customer_id)
    if not customer:
        return jsonify({"error": "Member not found."}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f'Member id: {customer_id}, successfully deleted.'}), 200

#Delete all customers
# @customers_bp.route("/", methods=['DELETE'])
# def delete_customers():
#     db.session.execute(delete(Customers))
#     db.session.commit()
#     return jsonify({"message":"customers has been deleted successfully"})