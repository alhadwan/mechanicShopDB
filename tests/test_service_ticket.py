from app import create_app 
from app.models import db, Customers
import unittest

class TestServiceTicket(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()

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
            self.customer_id = self.customer.id

    def test_create_serviceTicket(self):
        """Positive: valid serviceTicket is created"""
        serviceTicket = {
            "service_date": "2025-10-24",
            "service_desc": "Brake Technician",
            "vin": "1HGCM82633A639741",
            "customer_id": self.customer_id
        }

        response = self.client.post("/serviceTickets/", json=serviceTicket)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get("customer_id"), self.customer_id)

    def test_invalid_serviceTicket(self):
        """Negative: missing required vin"""
        serviceTicket = {
            "service_date": "2025-10-24",
            "service_desc": "Brake Technician",
            # "vin": "1HGCM82633A639741",
            "customer_id": self.customer_id
        }

        response = self.client.post("/serviceTickets/", json=serviceTicket)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json.get("vin"),
            ["Missing data for required field."]
        )

