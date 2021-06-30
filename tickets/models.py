from django.db import models

from users.models   import User
from flights.models import Flight

class Ticket(models.Model): 
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=50)
    flight        = models.ForeignKey(Flight, on_delete=models.CASCADE)
    
    class Meta: 
        db_table = 'tickets'

class Passenger(models.Model): 
    korean_name  = models.CharField(max_length=45)
    english_name = models.CharField(max_length=45)
    birth        = models.DateField()
    phone        = models.CharField(max_length=45)
    email        = models.EmailField(max_length=100)
    gender       = models.CharField(max_length=45)
    passport     = models.CharField(max_length=45)
    ticket       = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    pdf_url       = models.URLField(null=True)

    class Meta: 
        db_table = 'passengers'