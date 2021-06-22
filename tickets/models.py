from django.db import models

from users.models   import User
from flights.models import Flight

class Passenger(models.Model): 
    name_kor = models.CharField(max_length=45)
    name_eng = models.CharField(max_length=45)
    birth    = models.DateField()
    phone    = models.CharField(max_length=45)
    email    = models.EmailField(max_length=100)
    gender   = models.BooleanField()
    ticket   = models.ManyToManyField(Flight, through='Ticket')

    class Meta: 
        db_table = 'passengers'

class Ticket(models.Model): 
    user_id       = models.ForeignKey(User, on_delete=models.CASCADE)
    passenger_id  = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name="air_ticket")
    ticket_number = models.IntegerField()
    flight_id     = models.ForeignKey(Flight, on_delete=models.CASCADE)

    class Meta: 
        db_table = 'tickets'