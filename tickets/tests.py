import boto3, json, pdfkit

from datetime               import datetime
from django.views           import View
from django.http            import JsonResponse
from django.template.loader import get_template
from django.core.files.base import ContentFile
from django.test            import TestCase, Client

from tickets.models import Passenger
from my_settings    import AWS_ACCESS_KEY, AWS_SECRET_KEY
from tickets.models import Ticket
from flights.models import Flight, City, Country, FlightSeat, Seat
from users.models   import User

from .models        import Passenger, Ticket
from users.models   import User
from flights.models import Flight, City, Country, FlightSeat, Seat

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

class ReservationPostTest(TestCase):
    def setUp(self):
        User.objects.create(
            id           = 1,
            identity     = "abcabc",
            password     = "abc123!",
            korean_name  = "홍 길동",
            english_name = "HONG GILDONG",
            birth        = "1990-01-01",
            phone        = "01012341234",
            email        = "aaaa@gmail.com",
            gender       = "남자"
        )

        Country.objects.create(
            id   = 1,
            name = "대한민국"
        )

        departure_city=City.objects.create(
            id           = 1,
            name         = "서울 / 김포",
            airport_code = "GMP",
            country_id   = 1
        )
 
        arrival_city=City.objects.create(
            id           = 2,
            name         = "제주",
            airport_code = "CJU",
            country_id   = 1
        )

        Flight.objects.create(
            id                 = 1,
            flight_number      = "KA101",
            departure_datetime = "2021-07-02 07:05",
            arrival_datetime   = "2021-07-02 08:15",
            duration           = "01:10",
            departure_city     = departure_city,
            arrival_city       = arrival_city,
            price              = 100000
        )
        
        Seat.objects.create(
            id =1,
            name = 'economy',
            price_ratio =1
        )
        
        FlightSeat.objects.create(
            id        = 1,
            flight_id = 1,
            seat_id   = 1,
            stock     = 3
        )

        Ticket.objects.create(
            id            = 1,
            user_id       = 1,
            ticket_number = 65764000,
            flight_id     = 1
        )

        Passenger.objects.create(
            id           = 1,
            korean_name  = "홍 길순",
            english_name = "HONG GILSOON",
            birth        = "1990-01-02",
            phone        = "01012341235",
            email        = "aaab@gmail.com",
            gender       = "여자",
            passport     = "M12341235",
            ticket_id    = 1
        )
     
    def tearDown(self):
        Ticket.objects.all().delete()
        Flight.objects.all().delete()
        City.objects.all().delete()
        Country.objects.all().delete()
        Passenger.objects.all().delete()
        User.objects.all().delete()
    
    def test_reservation_post_wrong_seat_name(self):
        client=Client()
        reservation=  {
                "flight_id"  : 1,
                "seat_name"  : "eco",
                "passengers" : [ 
                    {
                        "korean_name"  : "홍 길순", 
                        "english_name" : "HONG GILSOON", 
                        "birth"        : "1990-01-02", 
                        "phone"        : "01012341235", 
                        "email"        : "aaab@gmail.com", 
                        "gender"       : "여자", 
                        "passport"     : "M12341236"
                    }
                ]
            }
        
        response = client.post('/tickets', json.dumps(reservation), content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'ERROR' : 'WRONG SEAT NAME'
            }
        )

    def test_reservation_post_no_seats_available(self):
        client=Client()
        reservation=  {
                "flight_id"  : 1,
                "seat_name"  : "economy",
                "passengers" : [ 
                    {
                        "korean_name"  : "홍 길순", 
                        "english_name" : "HONG GILSOON", 
                        "birth"        : "1990-01-02", 
                        "phone"        : "01012341235", 
                        "email"        : "aaab@gmail.com", 
                        "gender"       : "여자", 
                        "passport"     : "M12341236"
                    },
                    {
                        "korean_name"  : "홍 길순", 
                        "english_name" : "HONG GILSOON", 
                        "birth"        : "1990-01-02", 
                        "phone"        : "01012341235", 
                        "email"        : "aaab@gmail.com", 
                        "gender"       : "여자", 
                        "passport"     : "M12341237"
                    },
                    {
                        "korean_name"  : "홍 길순", 
                        "english_name" : "HONG GILSOON", 
                        "birth"        : "1990-01-02", 
                        "phone"        : "01012341235", 
                        "email"        : "aaab@gmail.com", 
                        "gender"       : "여자", 
                        "passport"     : "M12341238"
                    },
                    {
                        "korean_name"  : "홍 길순", 
                        "english_name" : "HONG GILSOON", 
                        "birth"        : "1990-01-02", 
                        "phone"        : "01012341235", 
                        "email"        : "aaab@gmail.com", 
                        "gender"       : "여자", 
                        "passport"     : "M12341239"
                    }
                ]
            }
        
        response = client.post('/tickets', json.dumps(reservation), content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'ERROR' : 'NOT ENOUGH SEATS AVAILABLE'
            }
        )

    def test_reservation_post_regex_test_failed(self):
        client=Client()
        reservation={
                "flight_id"  : 1,
                "seat_name"  : "economy",
                "passengers" : [ 
                    {
                        "korean_name"  : "hong", 
                        "english_name" : "HONG GILSOON", 
                        "birth"        : "1990-01-02", 
                        "phone"        : "01012341235", 
                        "email"        : "aaab@gmail.com", 
                        "gender"       : "여자", 
                        "passport"     : "M12341236"
                    }
                ]
            }
        
        response = client.post('/tickets', json.dumps(reservation), content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'ERROR' : 'INVALID FORMAT'
            }
        )

    def test_reservation_post_wrong_seat_name(self):
        client=Client()
        reservation=  {
                "flight_id"  : 1,
                "seat_name"  : "eco",
                "passengers" : [ 
                    {
                        "korean_name"  : "홍 길순", 
                        "english_name" : "HONG GILSOON", 
                        "birth"        : "1990-01-02", 
                        "phone"        : "01012341235", 
                        "email"        : "aaab@gmail.com", 
                        "gender"       : "여자", 
                        "passport"     : "M12341235"
                    }
                ]
            }

        response = client.post('/tickets', json.dumps(reservation), content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'ERROR' : 'WRONG SEAT NAME'
            }
        )
  
class ReservationSearchTest(TestCase):
    def setUp(self):
        client = Client()
        User.objects.create(
            id           = 1,
            identity     = "abcabc",
            password     = "abc123!",
            korean_name  = "홍 길동",
            english_name = "HONG GILDONG",
            birth        = "1990-01-01",
            phone        = "01012341234",
            email        = "aaaa@gmail.com",
            gender       = "남자"
        )

        Country.objects.create(
            id   = 1,
            name = "대한민국"
        )

        departure_city=City.objects.create(
            id           = 1,
            name         = "서울 / 김포",
            airport_code = "GMP",
            country_id   = 1
        )
 
        arrival_city=City.objects.create(
            id           = 2,
            name         = "제주",
            airport_code = "CJU",
            country_id   = 1
        )

        Flight.objects.create(
            id                 = 1,
            flight_number      = "KA101",
            departure_datetime = "2021-07-02 07:05",
            arrival_datetime   = "2021-07-02 08:15",
            duration           = "01:10",
            departure_city     = departure_city,
            arrival_city       = arrival_city,
            price              = 100000
        )
        
        Ticket.objects.create(
            id            = 1,
            user_id       = 1,
            ticket_number = 65764000,
            flight_id     = 1
        )

        Passenger.objects.create(
            id           = 1,
            korean_name  = "홍 길순",
            english_name = "HONG GILSOON",
            birth        = "1990-01-02",
            phone        = "01012341235",
            email        = "aaab@gmail.com",
            gender       = "여자",
            passport     = "M12341234",
            ticket_id    = 1
        )
     
    def tearDown(self):
        Ticket.objects.all().delete()
        Flight.objects.all().delete()
        City.objects.all().delete()
        Country.objects.all().delete()
        Passenger.objects.all().delete()
        User.objects.all().delete()
    
    def test_reservation_get_success(self):
        client   = Client()
        response = client.get('/tickets')
        
        self.assertEqual(response.json(),
           {
                'result' : 'SUCCESS', 
                'tickets': [
                   {
                      'id'                  : 1, 
                      'userId'              : 1, 
                      'ticketNumber'        : '65764000', 
                      'flightId'            : 1, 
                      'departureDatetime'   : '2021-07-02T07:05:00', 
                      'departureAirportCode': 'GMP', 
                      'arrivalAirportCode'  : 'CJU', 
                      'departureAirportName': '서울 / 김포', 
                      'arrivalAirportName'  : '제주', 
                      'passengerSameFlight' : 1
                    }
                ]
            } 
        )
        self.assertEqual(response.status_code, 200)
