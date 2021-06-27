import json, datetime

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from .models  import Country, Flight

class FlightCountryListView(View):
    def get(self,request) :
        result = []

        for country in Country.objects.all() :
            city_list = [{
                    'city_id'     :city.id,
                    'city_name'   :city.name,
                    'airport_code':city.airport_code
                } for city in country.city_set.all()]
            result.append({country.name:city_list})
        return JsonResponse({'country_list':result}, status=200)
            
class FlightListView(View):
    def get(self,request) :

        arrival_city_id    = request.GET.get('arrival_city_id',None)
        departure_city_id  = request.GET.get('departure_city_id',None)
        arrival_datetime   = request.GET.get('arrival_datetime',None)
        departure_datetime = request.GET.get('departure_datetime',None)
        seat_name          = request.GET.get('seat_name',None)
        
        today = datetime.datetime.now()

        flight_filter = Flight.objects.filter(
            Q(departure_city_id = departure_city_id)&
            Q(arrival_city_id = arrival_city_id)&
            Q(arrival_datetime__date = arrival_datetime)&
            Q(departure_datetime__date = departure_datetime) &
            Q(flight_seat_flight__seat__name = seat_name)&
            Q(departure_datetime__gt = today)
        )
        
        result=[
                    {       
                        'id'                    :index+1,
                        'flight_id'             :flight.id,
                        'flight_number'         :flight.flight_number,
                        'departure_datetime'    :flight.departure_datetime,
                        'arrival_datetime'      :flight.arrival_datetime,
                        'duration'              :flight.duration,
                        'price'                 :flight.price,
                        'departure_city_name'   :flight.departure_city.name,
                        'arrival_city_name'     :flight.arrival_city.name,
                        'departure_airport_code':flight.departure_city.airport_code,
                        'arrival_airport_code'  :flight.arrival_city.airport_code,
                        'seat_stock'            :flight.flight_seat_flight.get(seat__name=seat_name).stock
                    } for index,flight in enumerate(flight_filter)]

        return JsonResponse({'flights_view' :result}, status=200)
