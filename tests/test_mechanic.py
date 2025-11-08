from app import create_app
from app.models import db
import unittest

class TestMechanics(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        #  Initialize the test client for making requests to the app.
        self.client = self.app.test_client() 

    #test create mechanic
    def test_create_mechanic(self):
        """Positive: valid mechanic is created"""
        mechanic_payload = {
            "email": "ho1@gmail.com",
            "name": "Ho1",
            "phone": "4157530001",
            "specialties": "Brake Technician"
        }

        response = self.client.post("/mechanics/", json = mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Ho1')

    #test invalid create mechanic
    def test_invalid_mechanic(self):
        """Negative: missing required email"""
        mechanic_payload = {
            # "email": "ho1@gmail.com",
            "name": "Ho1",
            "phone": "4157530001",
            "specialties": "Brake Technician"
        }

        response = self.client.post("/mechanics/", json = mechanic_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ["Missing data for required field."])