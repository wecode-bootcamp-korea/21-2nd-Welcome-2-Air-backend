import json

from django.test import TestCase, Client

from .models        import Passenger, Ticket
from users.models   import User
from flights.models import Flight, City, Country

class ReservationPostTest(TestCase):
    def setUp(self):
        User.objects.create(
            id=1,
            identity     = "abcabc",
            password     = "abc123!",
            korean_name  = "홍 길동",
            english_name = "HONG GILDONG",
            birth        = "1990-01-01",
            phone        = "01012341234",
            email        = "aaaa@gmail.com",
            gender       = "남자"
        )

        Passenger.objects.create(
            id           = 1,
            korean_name  = "홍 길순",
            english_name = "HONG GILSOON",
            birth        = "1990-01-02",
            phone        = "01012341235",
            email        = "aaab@gmail.com",
            gender       = "여자",
            passport     = "M12341234"
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
            passenger_id  = 1,
            ticket_number = 65764000,
            flight_id     = 1,
            pdf_url       = "www.testpdf.com"
        )

    def tearDown(self):
        Ticket.objects.all().delete()
        Flight.objects.all().delete()
        City.objects.all().delete()
        Country.objects.all().delete()
        Passenger.objects.all().delete()
        User.objects.all().delete()
    
    def test_reservation_post_success(self):
        client = Client()
        response=client.post('/tickets', json.dumps({
            "korean_name"  : "홍 길순", 
            "english_name" : "HONG GILSOON",
            "birth"        : "1990-01-02",
            "phone"        : "01012341234",
            "email"        : "aaab@gmail.com",
            "gender"       : "여자",
            "passport"     : "M12341234",
            "user_id"      : 1,
            "passenger_id" : 1,
            "ticket_number": 65764000,
            "flight_id"    : 1,
            "pdf_url"      : "www.testpdf.com",
        }), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 
            {
                'result' : 'SUCCESS'
            }
        )
 
    def test_reservation_invalid_korean_name(self):
        client = Client()
        reservation={
            "korean_name"  : "I am Korean", 
            "english_name" : "HONG GILSOON",
            "birth"        : "1990-01-02",
            "phone"        : "01012341234",
            "email"        : "aaab@gmail.com",
            "gender"       : "여자",
            "passport"     : "M12341234",
            "user_id"      : 1,
            "passenger_id" : 1,
            "ticket_number": 65764000,
            "flight_id"    : 1,
            "pdf_url"      : "www.testpdf.com"
        }

        response = client.post('/tickets', json.dumps(reservation), content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'ERROR' : 'INVALID KOREAN NAME'
            }
        )

    def test_reservation_invalid_english_name(self):
        client = Client()
        reservation={
            "korean_name"  : "홍 길순", 
            "english_name" : "나는 한국인이다",
            "birth"        : "1990-01-02",
            "phone"        : "01012341234",
            "email"        : "aaab@gmail.com",
            "gender"       : "여자",
            "passport"     : "M12341234",
            "user_id"      : 1,
            "passenger_id" : 1,
            "ticket_number": 65764000,
            "flight_id"    : 1,
            "pdf_url"      : "www.testpdf.com"
        }
        response = client.post('/tickets', json.dumps(reservation), content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'ERROR' : 'INVALID ENGLISH NAME'
            }
        )

    def test_reservation_invalid_birth_date(self):
        client = Client()
        reservation={
            "korean_name"  : "홍 길순", 
            "english_name" : "HONG GILSOON",
            "birth"        : "1990",
            "phone"        : "01012341234",
            "email"        : "aaab@gmail.com",
            "gender"       : "여자",
            "passport"     : "M12341234",
            "user_id"      : 1,
            "passenger_id" : 1,
            "ticket_number": 65764000,
            "flight_id"    : 1,
            "pdf_url"      : "www.testpdf.com"
        }
        response = client.post('/tickets', json.dumps(reservation), content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'ERROR' : 'INVALID BIRTH DATE FORMAT'
            }
        )
    
    def test_reservation_invalid_email(self):
        client = Client()
        reservation={
            "korean_name"  : "홍 길순", 
            "english_name" : "HONG GILSOON",
            "birth"        : '1990-01-02',
            "phone"        : "01012341234",
            "email"        : "hong",
            "gender"       : "여자",
            "passport"     : "M12341234",
            "user_id"      : 1,
            "passenger_id" : 1,
            "ticket_number": 65764000,
            "flight_id"    : 1,
            "pdf_url"      : "www.testpdf.com"
        }
        response = client.post('/tickets', json.dumps(reservation), content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'ERROR' : 'INVALID EMAIL FORMAT'
            }
        )

    def test_reservation_invalid_phone_number(self):
        client = Client()
        reservation={
            "korean_name"  : "홍 길순", 
            "english_name" : "HONG GILSOON",
            "birth"        : '1990-01-02',
            "phone"        : "000",
            "email"        : "aaab@gmail.com",
            "gender"       : "여자",
            "passport"     : "M12341234",
            "user_id"      : 1,
            "passenger_id" : 1,
            "ticket_number": 65764000,
            "flight_id"    : 1,
            "pdf_url"      : "www.testpdf.com"
        }
        response = client.post('/tickets', json.dumps(reservation), content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'ERROR' : 'INVALID PHONE NUMBER FORMAT'
            }
        )
    def test_reservation_invalid_gender_format(self):
        client = Client()
        reservation={
            "korean_name"  : "홍 길순", 
            "english_name" : "HONG GILSOON",
            "birth"        : '1990-01-02',
            "phone"        : "01012341234",
            "email"        : "aaab@gmail.com",
            "gender"       : "여",
            "passport"     : "M12341234",
            "user_id"      : 1,
            "passenger_id" : 1,
            "ticket_number": 65764000,
            "flight_id"    : 1,
            "pdf_url"      : "www.testpdf.com"
        }
        response = client.post('/tickets', json.dumps(reservation), content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'ERROR' : 'INVALID GENDER FORMAT'
            }
        )
    def test_reservation_invalid_passport_number(self):
        client = Client()
        reservation={
            "korean_name"  : "홍 길순", 
            "english_name" : "HONG GILSOON",
            "birth"        : '1990-01-02',
            "phone"        : "01012341234",
            "email"        : "aaab@gmail.com",
            "gender"       : "여자",
            "passport"     : "123",
            "user_id"      : 1,
            "passenger_id" : 1,
            "ticket_number": 65764000,
            "flight_id"    : 1,
            "pdf_url"      : "www.testpdf.com"
        }
        response = client.post('/tickets', json.dumps(reservation), content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'ERROR' : 'INVALID PASSPORT NUMBER'
            }
        )
    def test_reservation_invalid_pdf_url(self):
        client = Client()
        reservation={
            "korean_name"  : "홍 길순", 
            "english_name" : "HONG GILSOON",
            "birth"        : '1990-01-02',
            "phone"        : "01012341234",
            "email"        : "aaab@gmail.com",
            "gender"       : "여자",
            "passport"     : "M12341234",
            "user_id"      : 1,
            "passenger_id" : 1,
            "ticket_number": 65764000,
            "flight_id"    : 1,
            "pdf_url"      : "no_url"
        }
        response = client.post('/tickets', json.dumps(reservation), content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'ERROR' : 'INVALID PDF URL'
            }
        )
    def test_reservation_post_non_existing_flight(self):
        client = Client()
        reservation={
            "korean_name"  : "홍 길순", 
            "english_name" : "HONG GILSOON",
            "birth"        : '1990-01-02',
            "phone"        : "01012341234",
            "email"        : "aaab@gmail.com",
            "gender"       : "여자",
            "passport"     : "M12341234",
            "user_id"      : 1,
            "passenger_id" : 1,
            "ticket_number": 65764000,
            "flight_id"    : 9999,
            "pdf_url"      : "www.testpdf.com"
        }
        response = client.post('/tickets', json.dumps(reservation), content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'ERROR' : 'FLIGHT NOT AVAILABLE'
            }
        )

    def test_reservation_post_key_error(self):
        client = Client()
        reservation={
            "korean_name"  : "홍 길순", 
            "english_name" : "HONG GILSOON",
            "birth"        : '1990-01-02',
            "phone"        : "01012341234",
            "email"        : "aaab@gmail.com",
        }
        response = client.post('/tickets', json.dumps(reservation), content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'ERROR' : 'INVALID KEY'
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

        Passenger.objects.create(
            id           = 1,
            korean_name  = "홍 길순",
            english_name = "HONG GILSOON",
            birth        = "1990-01-02",
            phone        = "01012341235",
            email        = "aaab@gmail.com",
            gender       = "여자",
            passport     = "M12341234"
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
            passenger_id  = 1,
            ticket_number = 65764000,
            flight_id     = 1,
            pdf_url       = "www.testpdf.com"
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
            'result': 'SUCCESS',
            'tickets': [
                {
                    'id'                    : 1, 
                    'user_id'               : 1, 
                    'korean_name'           : '홍 길순', 
                    'english_name'          : 'HONG GILSOON', 
                    'passenger_id'          : 1, 
                    'ticket_number'         : 65764000, 
                    'flight_id'             : 1, 
                    'departure_datetime'    : '2021-07-02T07:05:00', 
                    'departure_airport_code': 'GMP', 
                    'arrival_airport_code'  : 'CJU', 
                    'departure_airport_name': '서울 / 김포', 
                    'arrival_airport_name'  : '제주', 
                    'pdf_url'               : 'www.testpdf.com'
                }
            ]
        }
    )
        self.assertEqual(response.status_code, 200)
