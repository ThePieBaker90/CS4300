from django.urls import path
from . import views

urlpatterns = [
    path("", views.movie_list_page, name="movie_list"),
    path("movies/", views.movie_list_page, name="movie_list"),
    path("movies/<int:movie_id>/seats/", views.seat_booking_page, name="seat_booking"),
    path("my-bookings/", views.booking_history_page, name="booking_history"),
]