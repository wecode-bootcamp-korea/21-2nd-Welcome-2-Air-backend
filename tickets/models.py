from django.db import models

from users.models   import User
from flights.models import Flight

class Passenger(models.Model): 
    korean_name  = models.CharField(max_length=45)
    english_name = models.CharField(max_length=45)
    birth        = models.DateField()
    phone        = models.CharField(max_length=45)
    email        = models.EmailField(max_length=100)
    gender       = models.BooleanField()
    passport     = models.CharField(max_length=45)
    ticket       = models.ManyToManyField(Flight, through='Ticket')

    class Meta: 
        db_table = 'passengers'

class Ticket(models.Model): 
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    passenger     = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name="air_ticket")
    ticket_number = models.IntegerField()
    flight_id     = models.ForeignKey(Flight, on_delete=models.CASCADE)

    class Meta: 
        db_table = 'tickets'