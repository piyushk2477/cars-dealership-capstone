import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Dealer, Review

class DealershipApiTests(TestCase):
    def setUp(self):
        self.dealer = Dealer.objects.create(
            name="Test Motors", city="Austin", state="TX",
            address="100 Test Street", zip_code="78701"
        )

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
            "username": "capstone-user", "first_name": "Capstone", "last_name": "User",
            "email": "student@example.com", "password": "safe-pass-123"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username="capstone-user")
        self.assertEqual(user.first_name, "Capstone")

    def test_car_makes_endpoint_has_expected_shape(self):
        response = self.client.get("/djangoapp/get_cars")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload["CarModels"]), 15)
        self.assertEqual(payload["CarModels"][0], {"CarModel": "Pathfinder", "CarMake": "NISSAN"})

    def test_legacy_dealer_endpoints(self):
        response = self.client.get("/fetchDealers")
        self.assertEqual(response.status_code, 200)
        dealer = response.json()[0]
        for key in ("_id", "id", "city", "state", "address", "zip", "lat", "long", "short_name", "full_name", "__v"):
            self.assertIn(key, dealer)
        detail = self.client.get(f"/fetchDealer/{self.dealer.id}")
        self.assertEqual(detail.status_code, 200)
        self.assertEqual(detail.json()["id"], self.dealer.id)

    def test_legacy_state_filter_accepts_full_name(self):
        response = self.client.get("/fetchDealers/Texas")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["state"], "Texas")

    def test_legacy_sentiment_analysis(self):
        response = self.client.get("/analyze/Fantastic%20services")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"sentiment": "positive"})

    def test_legacy_logout_contract(self):
        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"userName": ""})

    def test_car_year_review_field(self):
        self.assertEqual(Review._meta.get_field("car_year").max_length, 4)

    def test_legacy_login_contract(self):
        User.objects.create_user(username="rubric-user", password="test-password")
        response = self.client.post("/login", data=json.dumps({
            "userName": "rubric-user", "password": "test-password"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"userName": "rubric-user", "status": "Authenticated"})
