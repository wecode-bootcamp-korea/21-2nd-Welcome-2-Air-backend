import boto3, json, pdfkit

from datetime               import datetime
from django.views           import View
from django.http            import JsonResponse
from django.template.loader import get_template
from django.core.files.base import ContentFile

from users.utils    import login_decorator
from tickets.models import Passenger
from my_settings    import AWS_ACCESS_KEY, AWS_SECRET_KEY

class TicketPdfView(View):

    s3_client = boto3.client(
        's3',
        aws_access_key_id     = AWS_ACCESS_KEY,
        aws_secret_access_key = AWS_SECRET_KEY
    )

    @login_decorator
    def post(self, request):
        data       = json.loads(request.body)
        ticket_id  = data['ticket_id']
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
                "duration"               : passenger.ticket.flight.duration,
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