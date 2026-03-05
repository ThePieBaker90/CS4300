from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import transaction

from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import HttpResponse

def movie_list_page(request):
    movies = Movie.objects.all().order_by("-release_date")
    return render(request, "bookings/movie_list.html", {"movies": movies})

@login_required
def booking_history_page(request):
    bookings = Booking.objects.filter(user=request.user).order_by("-booking_date")
    return render(request, "bookings/booking_history.html", {"bookings": bookings})

def seat_booking_page(request, movie_id):
    return HttpResponse(f"Seat booking page for movie {movie_id} (coming next)")

class MovieViewSet(viewsets.ModelViewSet):
    """
    CRUD for movies:
    GET /api/movies/
    POST /api/movies/
    GET /api/movies/{id}/
    PUT/PATCH /api/movies/{id}/
    DELETE /api/movies/{id}/
    """
    queryset = Movie.objects.all().order_by("-release_date")
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]  # public listings


class SeatViewSet(viewsets.ModelViewSet):
    """
    Seats: list/create/update seats (admin-like capability).
    Later we’ll mainly use it to view availability.
    """
    queryset = Seat.objects.all().order_by("seat_number")
    serializer_class = SeatSerializer
    permission_classes = [permissions.AllowAny]


class BookingViewSet(viewsets.ModelViewSet):
    """
    Bookings:
    - Auth required
    - Users can view only their own booking history
    - Creating a booking marks the seat as booked (prevents double booking)
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # booking history for the logged-in user only
        return Booking.objects.filter(user=self.request.user).order_by("-booking_date")

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        movie_id = request.data.get("movie")
        seat_id = request.data.get("seat")

        if not movie_id or not seat_id:
            return Response(
                {"detail": "movie and seat are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Lock the seat row so two requests can’t book it at once
        try:
            seat = Seat.objects.select_for_update().get(id=seat_id)
        except Seat.DoesNotExist:
            return Response({"detail": "Seat not found."}, status=status.HTTP_404_NOT_FOUND)

        if seat.is_booked:
            return Response(
                {"detail": "Seat is already booked."},
                status=status.HTTP_409_CONFLICT,
            )

        # Validate movie exists
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({"detail": "Movie not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create booking tied to the logged-in user
        booking = Booking.objects.create(user=request.user, movie=movie, seat=seat)

        # Mark seat booked
        seat.is_booked = True
        seat.save(update_fields=["is_booked"])

        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)