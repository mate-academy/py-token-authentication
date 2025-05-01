from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from cinema.models import CinemaHall
from cinema.serializers import CinemaHallSerializer
from user.tests.test_user_api import create_user

CINEMA_HALL_URL = reverse("cinema:cinemahall-list")


def sample_cinema_hall(**params):
    defaults = {
        "name": "test_hall",
        "rows": 10,
        "seats_in_row": 10,
    }
    defaults.update(params)

    return CinemaHall.objects.create(**defaults)


class PublicCinemaHallApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(CINEMA_HALL_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCinemaHallApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            username="test_admin",
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_cinema_halls(self):
        sample_cinema_hall()

        response = self.client.get(CINEMA_HALL_URL)

        cinema_halls = CinemaHall.objects.all()
        serializer = CinemaHallSerializer(cinema_halls, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_cinema_hall(self):
        payload = {
            "name": "test_hall",
            "rows": 10,
            "seats_in_row": 10,
        }

        response = self.client.post(CINEMA_HALL_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminCinemaHallApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            username="test_admin",
            email="test@test.com",
            password="testpass",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_post_cinema_hall(self):
        payload = {
            "name": "test_hall",
            "rows": 10,
            "seats_in_row": 10,
        }

        response = self.client.post(CINEMA_HALL_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_cinema_hall(self):
        cinema_hall = sample_cinema_hall()

        response = self.client.get(f"{CINEMA_HALL_URL}{cinema_hall.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_cinema_hall(self):
        cinema_hall = sample_cinema_hall()
        payload = {
            "name": "new_hall",
            "rows": 20,
            "seats_in_row": 20,
        }

        response = self.client.put(f"{CINEMA_HALL_URL}{cinema_hall.id}/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_cinema_hall(self):
        cinema_hall = sample_cinema_hall()

        response = self.client.delete(f"{CINEMA_HALL_URL}{cinema_hall.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
