from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from accounts.models import User
from inquiries.models import MeetingRequest

class HealthTests(TestCase):
    def test_liveness_uses_standard_envelope(self):
        response = APIClient().get("/api/v1/health/liveness/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertEqual(response.json()["data"]["status"], "alive")

    def test_all_list_endpoints_include_navigation_fields(self):
        response = APIClient().get("/api/v1/amenities/?page=1&page_size=1")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("count", body)
        self.assertIn("next", body)
        self.assertIn("previous", body)
        self.assertIsNone(body["previous"])

class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", email="admin@example.com", password="StrongPassword-903!", role=User.Role.SUPER_ADMIN)
    def test_login_and_me(self):
        client = APIClient(); login = client.post("/api/v1/auth/login/", {"email":"admin@example.com","password":"StrongPassword-903!"}, format="json")
        self.assertEqual(login.status_code, 200)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.json()['data']['access']}")
        self.assertEqual(client.get("/api/v1/auth/me/").status_code, 200)

class PublicFormTests(TestCase):
    def test_meeting_rejects_past_date(self):
        response = APIClient().post("/api/v1/meeting-requests/", {"customer_name":"Test Customer","phone":"01712345678","email":"customer@example.com","meeting_type":"SITE_VISIT","preferred_date":str(timezone.localdate()-timedelta(days=1)),"preferred_time":"10:00","message":"Visit"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(MeetingRequest.objects.count(), 0)
    def test_honeypot_rejects_bot(self):
        response = APIClient().post("/api/v1/contact-messages/", {"full_name":"Bot","email":"bot@example.com","message":"spam","website":"https://spam.invalid"}, format="json")
        self.assertEqual(response.status_code, 400)
