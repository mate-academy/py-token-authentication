from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from cinema.models import CinemaHall, Movie, MovieSession, Order, Ticket


ORDER_URL = "/api/cinema/orders/"


class CinemaAuthenticationContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="customer",
            password="testpass123",
        )
        cls.other_user = get_user_model().objects.create_user(
            username="other_customer",
            password="testpass123",
        )
        cls.staff_user = get_user_model().objects.create_user(
            username="staff",
            password="testpass123",
            is_staff=True,
        )
        cls.cinema_hall = CinemaHall.objects.create(
            name="Small hall",
            rows=3,
            seats_in_row=4,
        )
        cls.movie = Movie.objects.create(
            title="Original title",
            description="A movie used in API contract tests.",
            duration=100,
        )
        cls.movie_session = MovieSession.objects.create(
            show_time=timezone.now().replace(microsecond=0),
            movie=cls.movie,
            cinema_hall=cls.cinema_hall,
        )

    def setUp(self):
        self.client = APIClient()

    def authenticate_with_token(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def order_payload(self, row=1, seat=1):
        return {
            "tickets": [
                {
                    "row": row,
                    "seat": seat,
                    "movie_session": self.movie_session.id,
                }
            ]
        }

    def test_anonymous_cannot_create_order(self):
        response = self.client.post(
            ORDER_URL, self.order_payload(), format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Order.objects.exists())
        self.assertFalse(Ticket.objects.exists())

    def test_authenticated_customer_creates_order_and_ticket(self):
        self.authenticate_with_token(self.user)

        response = self.client.post(
            ORDER_URL, self.order_payload(), format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get()
        self.assertEqual(order.id, response.data["id"])
        self.assertEqual(order.user, self.user)
        ticket = Ticket.objects.get()
        self.assertEqual(ticket.order, order)
        self.assertEqual(ticket.movie_session, self.movie_session)
        self.assertEqual((ticket.row, ticket.seat), (1, 1))

    def test_order_owner_comes_from_token_even_when_payload_names_other_user(self):
        self.authenticate_with_token(self.user)
        payload = self.order_payload()
        payload["user"] = self.other_user.id

        response = self.client.post(ORDER_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.get().user, self.user)

    def test_token_lists_only_own_orders_for_customer_and_staff(self):
        customer_order = Order.objects.create(user=self.user)
        staff_order = Order.objects.create(user=self.staff_user)
        Order.objects.create(user=self.other_user)

        for user, expected_order in [
            (self.user, customer_order),
            (self.staff_user, staff_order),
        ]:
            with self.subTest(is_staff=user.is_staff):
                self.authenticate_with_token(user)

                response = self.client.get(ORDER_URL)

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data["count"], 1)
                self.assertEqual(
                    [order["id"] for order in response.data["results"]],
                    [expected_order.id],
                )

    def test_out_of_hall_ticket_is_rejected_without_saving_order_or_ticket(self):
        self.authenticate_with_token(self.user)

        for row, seat in [
            (0, 1),
            (self.cinema_hall.rows + 1, 1),
            (1, 0),
            (1, self.cinema_hall.seats_in_row + 1),
        ]:
            with self.subTest(row=row, seat=seat):
                response = self.client.post(
                    ORDER_URL,
                    self.order_payload(row=row, seat=seat),
                    format="json",
                )

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertFalse(Order.objects.exists())
                self.assertFalse(Ticket.objects.exists())

    def test_customer_cannot_patch_movie_session(self):
        self.authenticate_with_token(self.user)
        original_show_time = self.movie_session.show_time
        new_show_time = original_show_time + timedelta(hours=2)

        response = self.client.patch(
            f"/api/cinema/movie_sessions/{self.movie_session.id}/",
            {"show_time": new_show_time.isoformat()},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.movie_session.refresh_from_db()
        self.assertEqual(self.movie_session.show_time, original_show_time)

    def test_staff_can_patch_movie_session(self):
        self.authenticate_with_token(self.staff_user)
        new_show_time = self.movie_session.show_time + timedelta(hours=2)

        response = self.client.patch(
            f"/api/cinema/movie_sessions/{self.movie_session.id}/",
            {"show_time": new_show_time.isoformat()},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie_session.refresh_from_db()
        self.assertEqual(self.movie_session.show_time, new_show_time)

    def test_movie_patch_is_unavailable_even_for_staff(self):
        self.authenticate_with_token(self.staff_user)
        original_title = self.movie.title

        response = self.client.patch(
            f"/api/cinema/movies/{self.movie.id}/",
            {"title": "Changed title"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, original_title)
