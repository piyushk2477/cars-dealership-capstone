import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Dealer

class DealershipApiTests(TestCase):
    def setUp(self):
        self.dealer = Dealer.objects.create(name="Test Motors", city="Austin", state="TX")

    def test_get_dealers_returns_json(self):
        response = self.client.get("/djangoapp/get_dealers")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["dealers"][0]["name"], "Test Motors")

    def test_filter_dealers_by_state(self):
        response = self.client.get("/djangoapp/get_dealers_by_state/TX")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["dealers"]), 1)

    def test_missing_dealer_returns_404(self):
        response = self.client.get("/djangoapp/get_dealer_by_id/9999")
        self.assertEqual(response.status_code, 404)

    def test_register_user(self):
        response = self.client.post("/djangoapp/register", data=json.dumps({
            "username": "capstone-user", "email": "student@example.com", "password": "safe-pass-123"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="capstone-user").exists())

    def test_car_makes_endpoint(self):
        response = self.client.get("/djangoapp/get_all_car_makes")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Toyota", response.json()["car_makes"])
