from django.db import models
from django.contrib.auth.models import User

#Stores information about each movie
class Movie(models.Model):
    title = models.CharField(max_length=255) #the title, max 255 char
    description = models.TextField() #the description
    release_date = models.DateField() #the release date
    duration = models.IntegerField(help_text="Duration in minutes") #and the duration

    def __str__(self): #return title function
        return self.title

#Stores information about each seat
class Seat(models.Model): 
    seat_number = models.CharField(max_length=10) #the seat number, max 10 char
    is_booked = models.BooleanField(default=False) #and if it has been booked, this is defaulted to false for all new seats.

    def __str__(self): #return seat number function
        return self.seat_number

#Stores information about each booking
class Booking(models.Model):
    #this holds a movie, a seat and a user (which does not exist for now)
    #The on_delete cascase makes it so that the attatched data points are deleted 
    #properly if a booking is destroyed.
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #Holds our booking date which is the time this object was created.
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.movie} - {self.seat}"