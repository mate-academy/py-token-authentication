from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from cinema.models import Genre
from cinema.serializers import GenreSerializer
from user.tests.test_user_api import create_user

GENRE_URL = reverse("cinema:genre-list")


def sample_genre(**params):
    defaults = {
        "name": "test_genre",
    }
    defaults.update(params)

    return Genre.objects.create(**defaults)


class PublicGenreApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(GENRE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateGenreApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            username="test_admin",
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_genres(self):
        sample_genre()

        response = self.client.get(GENRE_URL)

        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_genre(self):
        payload = {
            "name": "test_genre",
        }

        response = self.client.post(GENRE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminGenreApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            username="test_admin",
            email="test@test.com",
            password="testpass",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_post_genre(self):
        payload = {
            "name": "test_genre",
        }

        response = self.client.post(GENRE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_genre(self):
        genre = sample_genre()

        response = self.client.get(f"{GENRE_URL}{genre.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_genre(self):
        genre = sample_genre()
        payload = {
            "name": "new_genre",
        }

        response = self.client.put(f"{GENRE_URL}{genre.id}/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_genre(self):
        genre = sample_genre()

        response = self.client.delete(f"{GENRE_URL}{genre.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
