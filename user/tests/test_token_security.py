"""Integration coverage using real token authentication headers."""
from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


class TokenSecurityTests(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="buyer", password="secure123"
        )

    def login(self) -> str:
        response = self.client.post(
            "/api/user/login/",
            {"username": "buyer", "password": "secure123"},
        )
        self.assertEqual(response.status_code, 200)
        return response.data["token"]

    def test_real_token_can_read_but_not_write_cinema(self) -> None:
        token = self.login()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        self.assertEqual(self.client.get("/api/cinema/genres/").status_code,
                         200)
        response = self.client.post(
            "/api/cinema/genres/", {"name": "Drama"}
        )
        self.assertEqual(response.status_code, 403)
        profile = self.client.get("/api/user/me/")
        self.assertEqual(profile.data["id"], self.user.pk)
        self.assertNotIn("password", profile.data)

    def test_invalid_token_is_rejected(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION="Token invalid")
        self.assertEqual(
            self.client.get("/api/user/me/").status_code, 401
        )

    def test_registration_cannot_grant_staff(self) -> None:
        response = self.client.post(
            "/api/user/register/",
            {"username": "new", "password": "12345", "is_staff": True},
        )
        self.assertEqual(response.status_code, 201)
        user = get_user_model().objects.get(username="new")
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password("12345"))

    def test_profile_cannot_grant_staff_or_change_id(self) -> None:
        token = self.login()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.patch(
            "/api/user/me/",
            {"is_staff": True, "id": self.user.pk + 1},
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_staff)
        self.assertEqual(response.data["id"], self.user.pk)

    def test_inactive_user_cannot_login(self) -> None:
        self.user.is_active = False
        self.user.save()
        response = self.client.post(
            "/api/user/login/",
            {"username": "buyer", "password": "secure123"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertNotIn("token", response.data)
