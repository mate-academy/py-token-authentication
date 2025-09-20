from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


def create_user(**params) -> object:
    """Helper function to create a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.create_user_url = reverse("user:create")
        self.token_url = reverse("user:token")
        self.me_url = reverse("user:me")

    def test_create_valid_user_success(self) -> None:
        """Test creating user with valid payload is successful"""
        payload = {
            "username": "test1user",
            "email": "tes1t@test.com",
            "password": "testpass",
        }

        res = self.client.post(self.create_user_url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_exists(self) -> None:
        """Test creating a user that already exists fails"""
        payload = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "testpass",
        }
        create_user(**payload)

        res = self.client.post(self.create_user_url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self) -> None:
        """Test that the password must be more than 5 characters"""
        payload = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "tst",
        }
        res = self.client.post(self.create_user_url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self) -> None:
        """Test that a token is created for the user"""
        payload = {
            "username": "test",
            "email": "test@test.com",
            "password": "test123",
        }
        create_user(**payload)

        res = self.client.post(self.token_url, payload)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self) -> None:
        """Test that token is not created if invalid credentials are given"""
        create_user(username="user12345", email="test@test.com", password="test123")
        payload = {
            "username": "user12345",
            "email": "test@test.com",
            "password": "wrong",
        }

        res = self.client.post(self.token_url, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self) -> None:
        """Test that token is not created if user doesn't exist"""
        payload = {
            "email": "test@test.com",
            "password": "test123",
        }
        res = self.client.post(self.token_url, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self) -> None:
        """Test that email and password are required"""
        res = self.client.post(self.token_url, {"email": 1, "password": ""})
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self) -> None:
        """Test that authentication is required for users"""
        res = self.client.get(self.me_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """TEST API requests that require authentication"""

    def setUp(self) -> None:
        self.user = create_user(
            username="test_admin",
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.me_url = reverse("user:me")

    def test_retrieve_profile_success(self) -> None:
        """Test retrieving profile for logged in user"""
        res = self.client.get(self.me_url)

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

    def test_post_me_not_allowed(self) -> None:
        """Test that POST is not allowed on the "me" url"""
        res = self.client.post(self.me_url, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile_self(self) -> None:
        """Test updating the user profile for authenticated user"""
        payload = {"username": "test_123", "password": "newpassword123"}
        res = self.client.patch(self.me_url, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, payload["username"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
