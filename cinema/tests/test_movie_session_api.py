import datetime

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from cinema.models import MovieSession, Movie, CinemaHall
from cinema.tests.test_actor_api import sample_actor
from cinema.tests.test_cinema_hall_api import sample_cinema_hall
from cinema.tests.test_genre_api import sample_genre
from cinema.tests.test_movie_api import sample_movie
from user.tests.test_user_api import create_user
from cinema.serializers import MovieSessionListSerializer

MOVIE_SESSION_URL = reverse("cinema:moviesession-list")


def sample_movie(**params):
    defaults = {
        "title": "Test Movie",
        "description": "Test Description",
        "duration": 120,
    }
    defaults.update(params)

    return Movie.objects.create(**defaults)


def sample_cinema_hall(**params):
    defaults = {
        "name": "Test Hall",
        "rows": 10,
        "seats_in_row": 10,
    }
    defaults.update(params)

    return CinemaHall.objects.create(**defaults)


def sample_movie_session(**params):
    defaults = {
        "show_time": "2022-09-02T00:00:00Z",
        "movie": sample_movie(),
        "cinema_hall": sample_cinema_hall(),
    }
    defaults.update(params)

    return MovieSession.objects.create(**defaults)


def detail_url(movie_session_id):
    return reverse("cinema:moviesession-detail", args=[movie_session_id])


class PublicMovieSessionApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(MOVIE_SESSION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMovieSessionApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            username="test_user",
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_movie_sessions(self):
        sample_movie_session()

        response = self.client.get(MOVIE_SESSION_URL)

        movie_sessions = MovieSession.objects.all()
        serializer = MovieSessionListSerializer(movie_sessions, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_movie_session(self):
        movie = sample_movie()
        cinema_hall = sample_cinema_hall()
        payload = {
            "show_time": "2022-09-02T00:00:00Z",
            "movie": movie.id,
            "cinema_hall": cinema_hall.id,
        }

        response = self.client.post(MOVIE_SESSION_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminMovieSessionApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            username="test_admin",
            email="test@test.com",
            password="testpass",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_post_movie_session(self):
        movie = sample_movie()
        cinema_hall = sample_cinema_hall()
        payload = {
            "show_time": "2022-09-02T00:00:00Z",
            "movie": movie.id,
            "cinema_hall": cinema_hall.id,
        }

        response = self.client.post(MOVIE_SESSION_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_movie_session(self):
        movie_session = sample_movie_session()

        response = self.client.get(f"{MOVIE_SESSION_URL}{movie_session.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_movie_session(self):
        movie_session = sample_movie_session()
        movie = sample_movie()
        cinema_hall = sample_cinema_hall()
        payload = {
            "show_time": "2022-09-03T00:00:00Z",
            "movie": movie.id,
            "cinema_hall": cinema_hall.id,
        }

        response = self.client.put(f"{MOVIE_SESSION_URL}{movie_session.id}/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_movie_session(self):
        movie_session = sample_movie_session()

        response = self.client.delete(f"{MOVIE_SESSION_URL}{movie_session.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
