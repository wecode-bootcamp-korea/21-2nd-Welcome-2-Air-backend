from django.db import models

class Country(models.Model): 
    name = models.CharField(max_length=45)
    
    class Meta:
        db_table = 'countries'

class City(models.Model):
    name         = models.CharField(max_length=45)
    airport_code = models.CharField(max_length=5)
    country_id   = models.ForeignKey(Country, on_delete=models.CASCADE)
   
    class Meta:
        db_table = 'cities'

class Seat(models.Model):
    name        = models.IntegerField()
    price_ratio = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'seats'

class Flight(models.Model): 
    flight_number     = models.CharField(max_length=20)
    departure_date    = models.DateField()
    arrival_date      = models.DateField()
    departure_time    = models.TimeField()
    arrival_time      = models.TimeField(max_length=20)
    duration          = models.TimeField(max_length=20)
    departure_city_id = models.ForeignKey(City, on_delete=models.CASCADE, related_name='departure')
    arrival_city_id   = models.ForeignKey(City, on_delete=models.CASCADE, related_name='arrival')
    price             = models.DecimalField(max_digits=18, decimal_places=2)
    flight_seat       = models.ManyToManyField(Seat, through='FlightSeat')

    class Meta:
        db_table = 'flights'

class FlightSeat(models.Model):

    flight_id = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='air_seat')
    seat_id   = models.ForeignKey(Seat, on_delete=models.CASCADE)
    stock     = models.IntegerField()

    class Meta:
        db_table = 'flight_seats'