from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from cinema.models import Genre
from user.tests.test_user_api import create_user
from cinema.serializers import GenreSerializer

GENRE_URL = reverse("cinema:genre-list")


def detail_url(genre_id):
    return reverse("cinema:genre-detail", args=[genre_id])


def sample_genres(**params):
    defaults = {
        "name": "Poem",
    }
    defaults.update(params)

    return Genre.objects.create(**defaults)


class PublicGenresApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(GENRE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateGenreApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            username="test_user_private_genre",
            email="test_private_genre@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_genres(self):
        sample_genres(name="Test Genre 1 for list")
        sample_genres(name="Test Genre 2 for list")

        response = self.client.get(GENRE_URL)

        genres = Genre.objects.all().order_by("name")
        serializer = GenreSerializer(genres, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_genres_forbidden_for_regular_user(self):
        payload = {"name": "New Genre by Regular User"}

        response = self.client.post(GENRE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminGenreApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            username="test_admin_genre",
            email="test_admin_genre@test.com",
            password="testpass",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_post_genres_success_for_admin(self):
        payload = {"name": "Action"}

        response = self.client.post(GENRE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        genre = Genre.objects.get(id=response.data["id"])
        self.assertEqual(payload["name"], genre.name)

    def test_retrieve_genre_detail_success_for_admin(self):
        genre = sample_genres(name="Sci-Fi for retrieve")

        url = detail_url(genre.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = GenreSerializer(genre)
        self.assertEqual(response.data, serializer.data)

    def test_put_genre_not_allowed(self):
        genre = sample_genres(name="Drama for PUT test")
        payload = {"name": "Updated Drama"}

        url = detail_url(genre.id)
        response = self.client.put(url, payload)

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_genre_not_allowed(self):
        genre = sample_genres(name="Comedy for DELETE test")

        url = detail_url(genre.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
