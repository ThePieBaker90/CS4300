import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_theater_booking.settings")
django.setup()