from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    path("", views.movie_list_page, name="movie_list"),
    path("movies/", views.movie_list_page, name="movie_list"),
    path("movies/<int:movie_id>/seats/", views.seat_booking_page, name="seat_booking"),  # next step
    path("my-bookings/", views.booking_history_page, name="booking_history"),
]

def seat_booking_page(request, movie_id):
    return HttpResponse(f"Seat booking page for movie {movie_id} (coming next)")