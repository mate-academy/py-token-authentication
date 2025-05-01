from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from cinema.models import Movie, Genre, Actor
from cinema.serializers import MovieListSerializer
from user.tests.test_user_api import create_user

MOVIE_URL = reverse("cinema:movie-list")


def sample_movie(**params):
    defaults = {
        "title": "Test Movie",
        "description": "Test Description",
        "duration": 120,
    }
    defaults.update(params)

    return Movie.objects.create(**defaults)


def sample_genre(**params):
    defaults = {
        "name": "Test Genre",
    }
    defaults.update(params)

    return Genre.objects.create(**defaults)


def sample_actor(**params):
    defaults = {
        "first_name": "Test",
        "last_name": "Actor",
    }
    defaults.update(params)

    return Actor.objects.create(**defaults)


class PublicMovieApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(MOVIE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMovieApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            username="test_user",
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_movies(self):
        sample_movie()

        response = self.client.get(MOVIE_URL)

        movies = Movie.objects.all()
        serializer = MovieListSerializer(movies, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_movie(self):
        payload = {
            "title": "Test Movie",
            "description": "Test Description",
            "duration": 120,
        }

        response = self.client.post(MOVIE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminMovieApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            username="test_admin",
            email="test@test.com",
            password="testpass",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_post_movie(self):
        genre = sample_genre()
        actor = sample_actor()
        payload = {
            "title": "Test Movie",
            "description": "Test Description",
            "duration": 120,
            "genres": [genre.id],
            "actors": [actor.id],
        }

        response = self.client.post(MOVIE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_movie(self):
        movie = sample_movie()

        response = self.client.get(f"{MOVIE_URL}{movie.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_movie(self):
        movie = sample_movie()
        genre = sample_genre()
        actor = sample_actor()
        payload = {
            "title": "New Movie",
            "description": "New Description",
            "duration": 150,
            "genres": [genre.id],
            "actors": [actor.id],
        }

        response = self.client.put(f"{MOVIE_URL}{movie.id}/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_movie(self):
        movie = sample_movie()

        response = self.client.delete(f"{MOVIE_URL}{movie.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
