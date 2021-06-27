import boto3, json, pdfkit

from datetime               import datetime
from django.views           import View
from django.http            import JsonResponse
from django.template.loader import get_template
from django.core.files.base import ContentFile
from django.test            import TestCase, Client

from users.utils    import login_decorator
from tickets.models import Passenger
from my_settings    import AWS_ACCESS_KEY, AWS_SECRET_KEY
from tickets.models import Ticket
from flights.models import Flight, Country, City
from users.models   import User
class TicketPdfTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            id           = 1,
            identity     = '',
            kakao_id     = '',
            password     = 'abc123!',
            korean_name  = '이 정민',
            english_name = 'LEE JUNGMIN',
            birth        = '1993.01.01',
            phone        = '1092525601',
            email        = 'jung56@gmail.com',
            gender       = '남자'
        )
        country = Country.objects.create(
            name = '대한민국'
        )
        city_a = City.objects.create(
            name         = '서울/김포',
            airport_code = 'GMP',
            country      = country
        )
        city_b = City.objects.create(
            name         = '제주',
            airport_code = 'CJU',
            country      = country
        )
        flight = Flight.objects.create(
            flight_number      = 'KA101',
            departure_datetime = '2021-07-02 08:15:00',
            arrival_datetime   = '2021-07-02 07:05:00',
            duration           = '01:10:00',
            departure_city     = city_a,
            arrival_city       = city_b,
            price              = 100000
        )
        ticket = Ticket.objects.create(
            id            = 1,
            user          = user,
            ticket_number = 12341234,
            flight        = flight
        )
        Passenger.objects.create(
            korean_name  = '박 창현',
            english_name = 'PARK CHANGHYUN',
            birth        = '1994-12-19',
            phone        = '1031082374',
            email        = 'busan@damnit.com',
            gender       = '남자',
            passport     = 'M12331239',
            ticket       = ticket,
            pdf_url      = 'https://s3.ap-northeast-2.amazonaws.com/welcome2air/welcome2air_tickets2021-07-01 05:27:56.022849'
        )
    def tearDown(self):
        User.objects.all().delete()
        Country.objects.all().delete()
        City.objects.all().delete()
        Flight.objects.all().delete()
        Ticket.objects.all().delete()
        Passenger.objects.all().delete()


    def test_ticket_pdf_get(self):
        client   = Client()
        response = client.get('/tickets/pdf?ticket_id=1')
        self.assertEqual(response.json(),

            {'passenger_info':[{
                  'korean_name'   : "박 창현",
                  'english_name'  : "PARK CHANGHYUN",
                  'pdf_url'       : 'https://s3.ap-northeast-2.amazonaws.com/welcome2air/welcome2air_tickets2021-07-01 05:27:56.022849'}]
            } 
        
    )