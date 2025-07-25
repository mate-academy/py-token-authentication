from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Тест публичных API (регистрация, логин)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        payload = {
            "username": "test1user",
            "email": "tes1t@test.com",
            "password": "testpass",
        }
        url = reverse("user:create")
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(username=payload["username"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_exists(self):
        payload = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "testpass",
        }
        create_user(**payload)
        url = reverse("user:create")
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        payload = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "123",
        }
        url = reverse("user:create")
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(get_user_model().objects.filter(
            username=payload["username"]).exists())

    def test_create_token_for_user(self):
        payload = {
            "username": "test",
            "password": "test123",
        }
        create_user(**payload)
        url = reverse("user:login")
        res = self.client.post(url, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        create_user(username="user12345", password="test123")
        payload = {
            "username": "user12345",
            "password": "wrong",
        }
        url = reverse("user:login")
        res = self.client.post(url, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        payload = {
            "username": "nouser",
            "password": "pass123",
        }
        url = reverse("user:login")
        res = self.client.post(url, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        url = reverse("user:login")
        res = self.client.post(url, {"username": "", "password": ""})

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        url = reverse("user:manage")
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Тесты, которые требуют авторизации"""

    def setUp(self):
        self.user = create_user(
            username="test_admin",
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        url = reverse("user:manage")
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data,
            {
                "id": self.user.id,
                "username": self.user.username,
                "email": self.user.email,
                "is_staff": self.user.is_staff,
            },
        )

    def test_post_me_not_allowed(self):
        url = reverse("user:manage")
        res = self.client.post(url, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile_self(self):
        url = reverse("user:manage")
        payload = {"username": "test_123", "password": "newpassword123"}
        res = self.client.patch(url, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, payload["username"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
