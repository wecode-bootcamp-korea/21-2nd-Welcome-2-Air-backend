import boto3, json, pdfkit, uuid

from datetime               import datetime
from django.views           import View
from django.http            import JsonResponse
from django.template.loader import get_template
from django.core.files.base import ContentFile

from users.utils    import login_decorator
from tickets.utils  import RegexValidator
from tickets.models import Passenger, Ticket
from flights.models import Flight, FlightSeat
from my_settings    import AWS_ACCESS_KEY, AWS_SECRET_KEY

class TicketPdfView(View):

    s3_client = boto3.client(
        's3',
        aws_access_key_id     = AWS_ACCESS_KEY,
        aws_secret_access_key = AWS_SECRET_KEY
    )

    @login_decorator
    def post(self, request):
        try:
            data       = json.loads(request.body)
            ticket_id  = data['ticket_id']

            if not Passenger.objects.filter(ticket_id=ticket_id).exists():
                return JsonResponse({'message':'INCORRECT_TICKET_ID'})
        
            passengers = Passenger.objects.filter(ticket_id = ticket_id)

            for passenger in passengers:
                content = {
                    "korean_name"            : passenger.korean_name,
                    "english_name"           : passenger.english_name,
                    "phone"                  : passenger.phone,
                    "passport"               : passenger.passport,
                    "flight_number"          : passenger.ticket.flight.flight_number,
                    "departure_datetime"     : passenger.ticket.flight.departure_datetime,
                    "arrival_datetime"       : passenger.ticket.flight.arrival_datetime,
                    "duration"               : passenger.ticket.flight.duration.strftime("%H:%M"),
                    "departure_city"         : passenger.ticket.flight.departure_city.name,
                    "arrival_city"           : passenger.ticket.flight.arrival_city.name,
                    "departure_country"      : passenger.ticket.flight.departure_city.country.name,
                    "arrival_country"        : passenger.ticket.flight.arrival_city.country.name,
                    "departure_airport_code" : passenger.ticket.flight.departure_city.airport_code,
                    "arrival_airport_code"   : passenger.ticket.flight.arrival_city.airport_code,
                    "price"                  : passenger.ticket.flight.price
                }

                template            = get_template('tickets/pdf.html')
                html                = template.render(content)
                pdf                 = pdfkit.from_string(html, False)
                ticket_pdf          = ContentFile(pdf)
                welcome2air_tickets = 'welcome2air_tickets'+str(datetime.now())

                self.s3_client.upload_fileobj(
                    ticket_pdf,
                    'welcome2air',
                    welcome2air_tickets,
                    ExtraArgs={
                        'ContentType' : 'application/pdf'
                    }
                )
            
                file_url = f"https://s3.ap-northeast-2.amazonaws.com/{'welcome2air'}/{welcome2air_tickets}"
            
                passenger.pdf_url = file_url
                passenger.save()

            return JsonResponse({'message':'SAVE_SUCESS'}, status= 201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status= 400)
    
    @login_decorator
    def get(self, request):
        ticket_id  = request.GET.get('ticket_id')

        if not Passenger.objects.filter(ticket_id=ticket_id).exists():
            return JsonResponse({'message':'INCORRECT_TICKET_ID'})

        passengers = Passenger.objects.filter(ticket_id=ticket_id)

        result = {'passenger_info':[{
                  'korean_name'   : passenger.korean_name,
                  'english_name'  :passenger.english_name,
                  'pdf_url'       : passenger.pdf_url
            } for passenger in passengers]
        }

        return JsonResponse(result, status=200)

class ReservationView(View):
    @login_decorator
    def post(self, request):
        data   = json.loads(request.body)
        user_id = request.user.id
        
        try:
            passengers = data['passengers']
            flight_id  = data['flight_id']
            seat_name  = data['seat_name']
      
            if not Flight.objects.filter(id=flight_id).exists():
                return JsonResponse({'ERROR' : 'FLIGHT NOT AVAILABLE'}, status=400)

            if not seat_name in ["economy", "business", "first"]:
                return JsonResponse({'ERROR' : 'WRONG SEAT NAME'}, status=400)
            
            flight_seat = FlightSeat.objects.get(seat__name=seat_name, flight_id=flight_id)
            
            ticket = Ticket.objects.create(
                    user_id       = user_id,
                    flight_id     = flight_id,
                    ticket_number = str(uuid.uuid4())
            )
 
            if flight_seat.stock < len(passengers):
                    return JsonResponse({'ERROR' : 'NOT ENOUGH SEATS AVAILABLE'}, status=400)
          
            for passenger in passengers:
                korean_name  = passenger['korean_name']
                english_name = passenger['english_name']
                birth        = passenger['birth']
                email        = passenger['email']
                phone        = passenger['phone']
                gender       = passenger['gender']
                passport     = passenger['passport']

                if RegexValidator(korean_name, english_name, birth, email, phone, gender, passport) == False:
                    return JsonResponse({'ERROR' : 'INVALID FORMAT'}, status=400)

                Passenger.objects.create(
                    korean_name  = korean_name,
                    english_name = english_name,
                    birth        = birth,
                    phone        = phone,
                    email        = email,
                    gender       = gender,
                    passport     = passport,
                    ticket_id    = ticket.id
                ) 

            flight_seat.stock -= len(passengers)
            flight_seat.save()
            
            return JsonResponse({'result' : 'SUCCESS', 'ticketNumber' : ticket.ticket_number, 'ticketId':ticket.id}, status=201)
        except KeyError:
            return JsonResponse({'ERROR' : 'INVALID KEY'}, status=400)

    @login_decorator
    def get(self, request):
        user_id = request.user.id
        result = [
            {
                    'ticketId'             : ticket.id,
                    'userId'               : user_id,
                    'ticketNumber'         : ticket.ticket_number,
                    'flightId'             : ticket.flight.id,
                    'departureDatetime'    : ticket.flight.departure_datetime,
                    'departureAirportCode' : ticket.flight.departure_city.airport_code,
                    'arrivalAirportCode'   : ticket.flight.arrival_city.airport_code,
                    'departureAirportName' : ticket.flight.departure_city.name,
                    'arrivalAirportName'   : ticket.flight.arrival_city.name,
                    'passengerSameFlight'  : ticket.passenger_set.count()
            } for ticket in Ticket.objects.filter(user_id=user_id)
        ]
        return JsonResponse({'result' : 'SUCCESS','tickets' : result }, status=200)