from app import create_app 
from app.models import db, Customers 
from app.utils.utils import encode_token
from datetime import datetime 
import unittest 

class TestCustomers(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.customer = Customers(
            name="test_customer",
            email="test@email.com",
            phone="6543246432",
            password="test"
        )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
        # self.token = encode_token(1)
        self.client = self.app.test_client()

#   test create customer
    def test_create_customer(self):
        """Positive: valid customer is created"""
        customer_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "1234567890",
            "password": "123"
        }

        response = self.client.post("/customers/", json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "John Doe")

#  test invalid create customer
    def test_invalid_creation(self):
        """Negative: missing required email"""
        customer_payload = {
            "name": "John Doe",
            # "email": "jd@email.com",
            "phone": "1234567890",
            "password": "123"
        }

        response = self.client.post("/customers/", json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json["email"],
            ["Missing data for required field."]
        )

    # test customer login
    def test_login_customer(self):
        """Positive: valid customer login"""
        credentials = {
            "email": "test@email.com",
            "password": "test"
        }

        response = self.client.post("/customers/login", json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
        self.assertIn("auth_token", response.json)
        return response.json["auth_token"]
    
    # test invalid customer login
    def test_invalid_login(self):
        """Negative: invalid customer login"""
        credentials = {
            "email": "test@email.com",
            "password": "wrongpassword"
        }

        response = self.client.post("/customers/login", json=credentials)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['error'], 'Invalid email or password.')

    # test update customer
    def test_update_customer(self):
        """Positive: valid customer update"""
        update_payload = {
            "name": "chen",
            "phone": "0987654321",
            "email": "test@email.com",
            "password": "test"
        }
        headers = {'Authorization': "Bearer " + self.test_login_customer()}

        response = self.client.put(f"/customers/", json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "chen")
        self.assertEqual(response.json["email"], "test@email.com")

    # test unauthorized update customer
    def test_unauthorized_update_customer(self):
        """Negative: unauthorized customer update"""
        update_payload = {
            "name": "chen",
            "phone": "0987654321",
            "email": "test@email.com",
            "password": "test"
        }   
        response = self.client.put(f"/customers/", json=update_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], ' You must be login to access this')

    def test_get_all_customer(self):
        """Positive: get all customers"""
        pagination_params = {"page": 1, "per_page": 1} 
        response = self.client.get("/customers/", query_string=pagination_params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_get_customer_by_id(self):
        """Positive: get customer by id"""
        response = self.client.get(f"/customers/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "test_customer")

    # test delete customer
    def test_delete_customer(self):
        """Positive: valid customer deletion"""
        headers = {'Authorization': "Bearer " + self.test_login_customer()}

        response = self.client.delete(f"/customers/", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], f'Customer id: 1, successfully deleted.')