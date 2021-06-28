import json, re, random

from django.http      import JsonResponse
from django.views     import View

from users.utils  import LoginStatus
from .models      import Passenger, Ticket

class ReservationPost(View):
    @LoginStatus
    def post(self, request):
        data    = json.loads(request.body)
        user_id = request.user.id

        try:
            korean_name  = data['korean_name']
            english_name = data['english_name']
            birth        = data['birth']
            email        = data['email']
            phone        = data['phone']
            gender       = data['gender']
            passport     = data['passport']
            
            KOREAN_REGEX       = "^[가-힣\s]+$"
            ENGLISH_NAME_REGEX = "^[a-zA-Z\s]+$"
            BIRTH_REGEX        = "^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$"
            EMAIL_REGEX        = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            PHONE_REGEX        = "^[0-9]{10,11}$"
            PASSPORT_REGEX     = "([a-zA-Z]{1}|[a-zA-Z]{2})\d{8}"

            if not re.search(KOREAN_REGEX, korean_name):
                return JsonResponse({'ERROR' : 'INVALID KOREAN NAME'}, status=400)
            if not re.search(ENGLISH_NAME_REGEX, english_name):
                return JsonResponse({'ERROR' : 'INVALID ENGLISH NAME'}, status=400)
            if not re.search(BIRTH_REGEX, birth):
                return JsonResponse({'ERROR' : 'INVALID BIRTH DATE FORMAT'}, status=400)
            if not re.search(EMAIL_REGEX, email):
                return JsonResponse({'ERROR' : 'INVALID EMAIL FORMAT'}, status=400)
            if not re.search(PHONE_REGEX, phone):
                return JsonResponse({'ERROR' : 'INVALID PHONE NUMBER FORMAT'}, status=400)
            if not gender=="남자" and not gender=="여자":
                return JsonResponse({'ERROR' : 'INVALID GENDER FORMAT'}, status=400)
            if not re.search(PASSPORT_REGEX, passport):
                return JsonResponse({'ERROR' : 'INVALID PASSPORT NUMBER'}, status=400)

            Passenger.objects.create(
                korean_name  = korean_name,
                english_name = english_name,
                birth        = birth,
                phone        = phone,
                email        = email,
                gender       = gender,
                passport     = passport
            )

            ticket_number = random.randint(10000000, 99999999)
            passenger_id  = data['passenger_id']
            flight_id     = data['flight_id']
            pdf_url       = data['pdf_url']

            PDF_URL_REGEX = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"

            if not re.search(PDF_URL_REGEX, pdf_url):
                return JsonResponse({'ERROR' : 'INVALID PDF URL'}, status=400)
            if not Ticket.objects.filter(flight_id=flight_id).exists():
                return JsonResponse({'ERROR' : 'FLIGHT NOT AVAILABLE'}, status=400)
            

            Ticket.objects.create(
                user_id         = user_id,
                passenger_id    = passenger_id,
                ticket_number   = ticket_number,
                flight_id       = flight_id,
                pdf_url         = pdf_url
            )
            return JsonResponse({'result' : 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'ERROR' : 'INVALID KEY'}, status=400)

class ReservationSearch(View):
    @LoginStatus
    def get(self, request):
        result = [ 
            {       
                    'id'                     : ticket.id,
                    'user_id'                : ticket.user_id,
                    'korean_name'            : ticket.passenger.korean_name,
                    'english_name'           : ticket.passenger.english_name,
                    'passenger_id'           : ticket.passenger_id,
                    'ticket_number'          : ticket.ticket_number,
                    'flight_id'              : ticket.flight_id,
                    'departure_datetime'     : ticket.flight.departure_datetime,
                    'departure_airport_code' : ticket.flight.departure_city.airport_code,
                    'arrival_airport_code'   : ticket.flight.arrival_city.airport_code,
                    'departure_airport_name' : ticket.flight.departure_city.name,
                    'arrival_airport_name'   : ticket.flight.arrival_city.name,
                    'pdf_url'                : ticket.pdf_url
            } for ticket in Ticket.objects.all()
        ]
        return JsonResponse({'result' : 'SUCCESS','tickets' : result }, status=200)