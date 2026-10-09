from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from cinema.models import Genre


CREATE_USER_URL = "/api/user/register/"
TOKEN_URL = "/api/user/login/"
ME_URL = "/api/user/me/"
GENRES_URL = "/api/cinema/genres/"


class UserContractTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def create_user(self, **overrides):
        params = {
            "username": "contract_user",
            "email": "contract@example.com",
            "password": "originalpass123",
        }
        params.update(overrides)
        return get_user_model().objects.create_user(**params)

    def test_registration_rejects_four_character_password(self):
        payload = {
            "username": "short_password_user",
            "email": "short@example.com",
            "password": "Ab12",
        }

        response = self.client.post(CREATE_USER_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertFalse(get_user_model().objects.exists())

    def test_registration_accepts_five_character_password_and_hides_it(self):
        payload = {
            "username": "minimum_password_user",
            "email": "minimum@example.com",
            "password": "Ab123",
        }

        response = self.client.post(CREATE_USER_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(username=payload["username"])
        self.assertNotEqual(user.password, payload["password"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertEqual(
            response.data,
            {
                "id": user.id,
                "username": payload["username"],
                "email": payload["email"],
                "is_staff": False,
            },
        )

    def test_registration_and_profile_patch_cannot_grant_staff_access(self):
        payload = {
            "username": "regular_user",
            "email": "regular@example.com",
            "password": "regularpass123",
            "is_staff": True,
        }

        response = self.client.post(CREATE_USER_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(username=payload["username"])
        self.assertFalse(user.is_staff)
        self.assertFalse(response.data["is_staff"])

        self.client.force_authenticate(user=user)
        response = self.client.patch(ME_URL, {"is_staff": True}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertFalse(user.is_staff)
        self.assertFalse(response.data["is_staff"])

    def test_email_patch_preserves_existing_password(self):
        user = self.create_user()
        original_password_hash = user.password
        self.client.force_authenticate(user=user)

        response = self.client.patch(
            ME_URL, {"email": "changed@example.com"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.email, "changed@example.com")
        self.assertEqual(user.password, original_password_hash)
        self.assertTrue(user.check_password("originalpass123"))
        self.assertNotIn("password", response.data)

    def test_put_updates_only_authenticated_user_and_hashes_password(self):
        other_user = self.create_user(
            username="other_user", email="other@example.com"
        )
        other_original_state = (
            other_user.username,
            other_user.email,
            other_user.password,
            other_user.is_staff,
        )
        user = self.create_user()
        self.client.force_authenticate(user=user)
        payload = {
            "username": "updated_user",
            "email": "updated@example.com",
            "password": "updatedpass123",
        }

        response = self.client.put(ME_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.username, payload["username"])
        self.assertEqual(user.email, payload["email"])
        self.assertNotEqual(user.password, payload["password"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertFalse(user.check_password("originalpass123"))
        self.assertEqual(response.data["id"], user.id)
        self.assertNotIn("password", response.data)
        other_user.refresh_from_db()
        self.assertEqual(
            (
                other_user.username,
                other_user.email,
                other_user.password,
                other_user.is_staff,
            ),
            other_original_state,
        )

    def test_username_login_token_authenticates_profile_and_genres(self):
        user = self.create_user()
        genre = Genre.objects.create(name="Action")
        self.assertEqual(
            self.client.get(GENRES_URL).status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        response = self.client.post(
            TOKEN_URL,
            {"username": user.username, "password": "originalpass123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["token"])
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {response.data['token']}"
        )
        profile_response = self.client.get(ME_URL)
        genres_response = self.client.get(GENRES_URL)

        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            profile_response.data,
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_staff": False,
            },
        )
        self.assertEqual(genres_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            genres_response.data, [{"id": genre.id, "name": genre.name}]
        )

    def test_invalid_token_is_rejected(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalid-token")

        for url in (ME_URL, GENRES_URL):
            with self.subTest(url=url):
                response = self.client.get(url)

                self.assertEqual(
                    response.status_code, status.HTTP_401_UNAUTHORIZED
                )

    def test_inactive_user_cannot_get_login_token(self):
        user = self.create_user(is_active=False)

        response = self.client.post(
            TOKEN_URL,
            {"username": user.username, "password": "originalpass123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", response.data)
