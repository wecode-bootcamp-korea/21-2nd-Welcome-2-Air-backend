import json, re, uuid


from django.http  import JsonResponse
from django.views import View
from django.db.models import F

from users.utils    import login_decorator
from .models        import Passenger, Ticket
from flights.models import Flight, FlightSeat, Seat
from tickets.utils  import RegexValidator


class ReservationView(View):
    @login_decorator
    def post(self, request):
        datas = json.loads(request.body)

        user_id = request.user.id
        try:
            reservation = datas['reservation']
            for information in reservation:
                flight_id     = information['flight_id']

                if not Flight.objects.filter(id=flight_id).exists():
                    return JsonResponse({'ERROR' : 'FLIGHT NOT AVAILABLE'}, status=400)
                
                korean_name  = information['korean_name']
                english_name = information['english_name']
                birth        = information['birth']
                email        = information['email']
                phone        = information['phone']
                gender       = information['gender']
                passport     = information['passport']
                seat_name    = information['seat_name']

                if RegexValidator(korean_name, english_name, birth, email, phone, gender, passport) == False:
                    return JsonResponse({'ERROR' : 'INVALID FORMAT'}, status=400)

                if Passenger.objects.filter(passport=passport).exists() and Ticket.objects.filter(flight_id=flight_id).exists():
                    return JsonResponse({'ERROR' : 'SAME PERSON TRYING TO BE ON THE SAME FLIGHT'}, status=400)

                seat_id = Seat.objects.get(name=seat_name).id
                stock =  FlightSeat.objects.filter(seat_id=seat_id).filter(flight_id=flight_id).first().stock

                if stock<=0:
                    return JsonResponse({'ERROR' : 'NOT ENOUGH SEATS AVAILABLE'}, status=400)

                ticket_number = str(uuid.uuid4().int)[:8]

                Ticket.objects.create(
                    user_id         = user_id,
                    flight_id       = flight_id,
                    ticket_number   = ticket_number
                )

                ticket_id = Ticket.objects.filter(flight_id=flight_id).last().id

                Passenger.objects.create(
                    korean_name  = korean_name,
                    english_name = english_name,
                    birth        = birth,
                    phone        = phone,
                    email        = email,
                    gender       = gender,
                    passport     = passport,
                    ticket_id    = ticket_id
                ) 

                FlightSeat.objects.filter(seat_id=seat_id).filter(flight_id=flight_id).update(stock=F('stock') - 1)
                
            return JsonResponse({'result' : 'SUCCESS', 'ticketNumber' : ticket_number}, status=201)
        except KeyError:
            return JsonResponse({'ERROR' : 'INVALID KEY'}, status=400)

    @login_decorator
    def get(self, request):
        user_id = request.user.id
        result = [
            {
                    'id'                     : passenger.id,
                    'user_id'                : user_id,
                    'korean_name'            : passenger.korean_name,
                    'english_name'           : passenger.english_name,
                    'ticket_number'          : passenger.ticket.ticket_number,
                    'flight_id'              : passenger.ticket.flight.id,
                    'departure_datetime'     : passenger.ticket.flight.departure_datetime,
                    'departure_airport_code' : passenger.ticket.flight.departure_city.airport_code,
                    'arrival_airport_code'   : passenger.ticket.flight.arrival_city.airport_code,
                    'departure_airport_name' : passenger.ticket.flight.departure_city.name,
                    'arrival_airport_name'   : passenger.ticket.flight.arrival_city.name,
                    'pdf_url'                : passenger.ticket.pdf_url,
                    'ticket_id'              : passenger.ticket_id
            } for passenger in Passenger.objects.all()
        ]
        return JsonResponse({'result' : 'SUCCESS','tickets' : result }, status=200)