from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from bookings.models import Movie, Seat, Booking

from django.urls import reverse


#Tests created by Artificial Intelligence.
#Integration Tests
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

#Make sure the template pages actually work (also ai coded)
class TemplatePageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u1", password="pass12345")

        self.movie = Movie.objects.create(
            title="Dune Part Two",
            description="Sci-fi epic",
            release_date="2024-03-01",
            duration=166,
        )
        self.seat_a1 = Seat.objects.create(seat_number="A1", is_booked=False)

    def test_movie_list_page_loads(self):
        resp = self.client.get(reverse("movie_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Now Showing")
        self.assertContains(resp, "Dune Part Two")

    def test_seat_booking_requires_login(self):
        url = reverse("seat_booking", kwargs={"movie_id": self.movie.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/login/", resp["Location"])

    def test_seat_booking_post_creates_booking_and_marks_seat(self):
        self.client.login(username="u1", password="pass12345")

        url = reverse("seat_booking", kwargs={"movie_id": self.movie.id})
        resp = self.client.post(url, {"seat_id": self.seat_a1.id})

        # Should redirect to booking history after success
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"], reverse("booking_history"))

        self.seat_a1.refresh_from_db()
        self.assertTrue(self.seat_a1.is_booked)
        self.assertEqual(Booking.objects.count(), 1)

    def test_booking_history_page_shows_users_bookings(self):
        Booking.objects.create(user=self.user, movie=self.movie, seat=self.seat_a1)
        self.seat_a1.is_booked = True
        self.seat_a1.save()

        self.client.login(username="u1", password="pass12345")
        resp = self.client.get(reverse("booking_history"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "My Booking History")
        self.assertContains(resp, "Dune Part Two")
        self.assertContains(resp, "A1")