from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class TokenSecurityTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="customer", password="secret123"
        )

    def test_login_token_authenticates_real_requests(self) -> None:
        response = self.client.post(
            reverse("user:login"),
            {"username": "customer", "password": "secret123"},
        )
        self.assertEqual(response.status_code, 200)
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.get(reverse("user:manage"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.user.pk)
        self.assertNotIn("password", response.data)
        self.assertEqual(
            self.client.get(reverse("cinema:genre-list")).status_code, 200
        )
        self.assertEqual(
            self.client.post(
                reverse("cinema:genre-list"), {"name": "Drama"}
            ).status_code,
            403,
        )

    def test_invalid_token_is_rejected(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION="Token invalid")
        response = self.client.get(reverse("user:manage"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response["WWW-Authenticate"], "Token")

    def test_registration_cannot_grant_staff_access(self) -> None:
        response = self.client.post(
            reverse("user:create"),
            {
                "username": "new",
                "password": "12345",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        self.assertEqual(response.status_code, 201)
        user = get_user_model().objects.get(username="new")
        self.assertTrue(user.check_password("12345"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_profile_cannot_grant_staff_access_or_change_other_users(self):
        other = get_user_model().objects.create_user(
            username="other", password="otherpass"
        )
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = self.client.patch(
            reverse("user:manage"),
            {"id": other.pk, "is_staff": True, "is_superuser": True},
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        other.refresh_from_db()
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertEqual(response.data["id"], self.user.pk)
        self.assertEqual(other.username, "other")

    def test_short_password_update_is_rejected(self) -> None:
        self.client.force_authenticate(self.user)
        response = self.client.patch(
            reverse("user:manage"), {"password": "1234"}
        )
        self.assertEqual(response.status_code, 400)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("secret123"))

    def test_inactive_user_cannot_login_or_use_token(self) -> None:
        token = Token.objects.create(user=self.user)
        self.user.is_active = False
        self.user.save()
        response = self.client.post(
            reverse("user:login"),
            {"username": "customer", "password": "secret123"},
        )
        self.assertEqual(response.status_code, 400)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self.assertEqual(
            self.client.get(reverse("user:manage")).status_code, 401
        )
