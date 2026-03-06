from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from bookings.models import Movie, Seat, Booking

#Tests created by Artificial Intelligence.
class MovieSeatBookingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Users
        self.user1 = User.objects.create_user(username="u1", password="pass12345")
        self.user2 = User.objects.create_user(username="u2", password="pass12345")

        # Movie + Seats
        self.movie = Movie.objects.create(
            title="Dune Part Two",
            description="Sci-fi epic",
            release_date="2024-03-01",
            duration=166,
        )
        self.seat_a1 = Seat.objects.create(seat_number="A1", is_booked=False)
        self.seat_a2 = Seat.objects.create(seat_number="A2", is_booked=False)

    def test_movies_list_public(self):
        resp = self.client.get("/api/movies/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.json()), 1)

    def test_booking_requires_auth(self):
        resp = self.client.post("/api/bookings/", {"movie": self.movie.id, "seat": self.seat_a1.id}, format="json")
        self.assertIn(resp.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_create_booking_marks_seat_booked(self):
        self.client.login(username="u1", password="pass12345")

        resp = self.client.post(
            "/api/bookings/",
            {"movie": self.movie.id, "seat": self.seat_a1.id},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        self.seat_a1.refresh_from_db()
        self.assertTrue(self.seat_a1.is_booked)
        self.assertEqual(Booking.objects.count(), 1)

    def test_cannot_double_book_same_seat(self):
        self.client.login(username="u1", password="pass12345")
        resp1 = self.client.post("/api/bookings/", {"movie": self.movie.id, "seat": self.seat_a1.id}, format="json")
        self.assertEqual(resp1.status_code, status.HTTP_201_CREATED)

        # Attempt second booking on same seat
        resp2 = self.client.post("/api/bookings/", {"movie": self.movie.id, "seat": self.seat_a1.id}, format="json")
        self.assertEqual(resp2.status_code, status.HTTP_409_CONFLICT)

    def test_booking_history_only_returns_logged_in_users_bookings(self):
        # Make a booking for user1
        Booking.objects.create(user=self.user1, movie=self.movie, seat=self.seat_a2)
        self.seat_a2.is_booked = True
        self.seat_a2.save()

        # user2 logs in and should see none
        self.client.login(username="u2", password="pass12345")
        resp = self.client.get("/api/bookings/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json(), [])