from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from cinema.models import Ticket, Order, MovieSession, Movie, CinemaHall
from cinema.serializers import OrderListSerializer
from user.tests.test_user_api import create_user

ORDER_URL = reverse("cinema:order-list")


def sample_movie_session(**params):
    defaults = {
        "show_time": "2022-09-02T00:00:00Z",
        "movie": Movie.objects.create(
            title="Test Movie",
            description="Test Description",
            duration=120,
        ),
        "cinema_hall": CinemaHall.objects.create(
            name="Test Hall",
            rows=10,
            seats_in_row=10,
        ),
    }
    defaults.update(params)

    return MovieSession.objects.create(**defaults)


def sample_order(user, **params):
    defaults = {
        "user": user,
    }
    defaults.update(params)

    return Order.objects.create(**defaults)


def sample_ticket(order, movie_session, **params):
    defaults = {
        "movie_session": movie_session,
        "order": order,
        "row": 1,
        "seat": 1,
    }
    defaults.update(params)

    return Ticket.objects.create(**defaults)


class PublicOrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ORDER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOrderApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            username="test_user",
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_orders(self):
        order = sample_order(user=self.user)
        movie_session = sample_movie_session()
        sample_ticket(order=order, movie_session=movie_session)

        response = self.client.get(ORDER_URL)

        orders = Order.objects.filter(user=self.user)
        serializer = OrderListSerializer(orders, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_post_order(self):
        movie_session = sample_movie_session()
        payload = {
            "tickets": [
                {
                    "movie_session": movie_session.id,
                    "row": 1,
                    "seat": 1,
                }
            ]
        }

        response = self.client.post(ORDER_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_order(self):
        order = sample_order(user=self.user)
        movie_session = sample_movie_session()
        sample_ticket(order=order, movie_session=movie_session)

        response = self.client.get(f"{ORDER_URL}{order.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_order(self):
        order = sample_order(user=self.user)
        movie_session = sample_movie_session()
        sample_ticket(order=order, movie_session=movie_session)

        new_movie_session = sample_movie_session()
        payload = {
            "tickets": [
                {
                    "movie_session": new_movie_session.id,
                    "row": 2,
                    "seat": 2,
                }
            ]
        }

        response = self.client.put(f"{ORDER_URL}{order.id}/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        order = sample_order(user=self.user)
        movie_session = sample_movie_session()
        sample_ticket(order=order, movie_session=movie_session)

        response = self.client.delete(f"{ORDER_URL}{order.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AdminOrderApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            username="test_admin",
            email="admin@test.com",
            password="testpass",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_order_when_admin_dont_have_order(self):
        user = create_user(
            username="test_user2",
            email="test2@test.com",
            password="testpass",
        )
        order = sample_order(user=user)
        movie_session = sample_movie_session()
        sample_ticket(order=order, movie_session=movie_session)

        response = self.client.get(f"{ORDER_URL}{order.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
