from behave import given, when, then
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from bookings.models import Movie, Seat


@given("a movie exists")
def step_movie_exists(context):
    context.movie = Movie.objects.create(
        title="Test Movie",
        description="Test description",
        release_date="2024-01-01",
        duration=120
    )


@given("a seat is available")
def step_seat_available(context):
    context.seat = Seat.objects.create(seat_number="A1", is_booked=False)


@given("the user is logged in")
def step_user_logged_in(context):
    user, created = User.objects.get_or_create(username="bdduser")
    if created:
        user.set_password("pass12345")
        user.save()

    context.user = user
    context.client = APIClient()
    context.client.login(username="bdduser", password="pass12345")


@when("the user books the seat")
def step_book_seat(context):
    context.response = context.client.post(
        "/api/bookings/",
        {"movie": context.movie.id, "seat": context.seat.id},
        format="json"
    )


@then("the seat should be marked as booked")
def step_verify_seat_booked(context):
    context.seat.refresh_from_db()
    assert context.seat.is_booked is True