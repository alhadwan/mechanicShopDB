from app import create_app
from app.models import db
import unittest

class TestInventories(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    # test create inventory    
    def test_create_inventory(self):
        """Positive: valid inventory is created"""
        inventory_payload = {
                "part_name": "Drain plug gasket",
                "price": 3.32
        }

        response = self.client.post("/inventory/", json=inventory_payload) 
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["price"], 3.32)

    # test invalid create  inventory    
    def test_invalid_inventory(self):
        """Negative: missing required price"""
        inventory_payload = {
                "part_name": "Drain plug gasket",
                # "price": 3.32
        }

        response = self.client.post("/inventory/", json=inventory_payload) 
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["price"], ["Missing data for required field."])
