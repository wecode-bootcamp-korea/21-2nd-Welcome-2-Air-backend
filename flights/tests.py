from django.test      import TestCase, Client

from .models  import Country, Flight, FlightSeat, Seat, City

class FlightCountryListViewTest(TestCase):
    def setUp(self):
        client = Client() # 가상의 db

        Country.objects.create(
            id   = 1,
            name = "대한민국"
        )
        City.objects.create(
            id           = 1,
            name         = "서울/김포",
            airport_code = "GMP",
            country_id   = 1
        )
        City.objects.create(
            id           = 2,
            name         = "제주",
            airport_code = "CJU",
            country_id   = 1
        )
        City.objects.create(
            id           = 3,
            name         = "부산/김해",
            airport_code = "PUS",
            country_id   = 1
        )
        City.objects.create(
            id           = 4,
            name         = "청주",
            airport_code = "CJJ",
            country_id   = 1
        )

    def tearDown(self) :
        Country.objects.all().delete()
        City.objects.all().delete()
        Flight.objects.all().delete()
        FlightSeat.objects.all().delete()
        Seat.objects.all().delete()

    def test_city_list(self) :
        client = Client()
        response = client.get('/flights/country')

        self.assertEqual(response.json(),
            {
                "country_list": [
                    {
                        "대한민국": [
                            {
                                "city_id": 1,
                                "city_name": "서울/김포",
                                "airport_code": "GMP"
                            },
                            {
                                "city_id": 2,
                                "city_name": "제주",
                                "airport_code": "CJU"
                            },
                            {
                                "city_id": 3,
                                "city_name": "부산/김해",
                                "airport_code": "PUS"
                            },
                            {
                                "city_id": 4,
                                "city_name": "청주",
                                "airport_code": "CJJ"
                            }
                        ]
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)



class FlightListViewTest(TestCase):
    def setUp(self):
        client = Client() # 가상의 db

        Country.objects.create(
            id   = 1,
            name = "대한민국"
        )
        a = City.objects.create(
            id           = 1,
            name         = "서울/김포",
            airport_code = "GMP",
            country_id   = 1
        )
        b = City.objects.create(
            id           = 2,
            name         = "제주",
            airport_code = "CJU",
            country_id   = 1
        )
        Seat.objects.create(
            id = 1,
            name = 'economy',
            price_ratio = 1.00,

        )
        Seat.objects.create(
            id = 2,
            name = 'business',
            price_ratio = 1.50,

        )
        Seat.objects.create(
            id = 3,
            name = 'first',
            price_ratio = 3.00,

        )

        Flight.objects.create(
            id                 = 1,
            flight_number      = "KA101",
            departure_datetime = "2021-07-03 07:05",
            arrival_datetime   = "2021-07-03 08:15",
            duration           = "01:10",
            departure_city     = b,
            arrival_city       = a,
            price              = 100000.00
        )
        Flight.objects.create(
            id                 = 2,
            flight_number      = "KA102",
            departure_datetime = "2021-07-03 08:05",
            arrival_datetime   = "2021-07-03 09:15",
            duration           = "01:10",
            departure_city     = b,
            arrival_city       = a,
            price              = 100000.00
        )
        FlightSeat.objects.create(
            id        = 1,
            stock     = 10,
            flight_id = 1,
            seat_id   = 1,
        )
        FlightSeat.objects.create(
            id        = 2,
            stock     = 8,
            flight_id = 1,
            seat_id   = 2,
        )
        
        FlightSeat.objects.create(
            id        = 3,
            stock     = 5,
            flight_id = 1,
            seat_id   = 3,
        )
        FlightSeat.objects.create(
            id        = 4,
            stock     = 10,
            flight_id = 2,
            seat_id   = 1,
        )
        FlightSeat.objects.create(
            id        = 5,
            stock     = 8,
            flight_id = 2,
            seat_id   = 2,
        )
        FlightSeat.objects.create(
            id        = 6,
            stock     = 5,
            flight_id = 2,
            seat_id   = 3,
        )

    def tearDown(self) :
        Country.objects.all().delete()
        City.objects.all().delete()
        Flight.objects.all().delete()
        FlightSeat.objects.all().delete()
        Seat.objects.all().delete()

    def test_city_list(self) :
        client = Client()
        response = client.get('/flights?arrival_city_id=1&departure_city_id=2&arrival_datetime=2021-07-03&departure_datetime=2021-07-03&seat_name=first')

        self.assertEqual(response.json(),
            {
                    "flights_view": [
                        {
                            "id": 1,
                            "flight_id": 1,
                            "flight_number": "KA101",
                            "departure_datetime": "2021-07-03T07:05:00",
                            "arrival_datetime": "2021-07-03T08:15:00",
                            "duration": "01:10:00",
                            "price": "100000.00",
                            "departure_city_name": "제주",
                            "arrival_city_name": "서울/김포",
                            "departure_airport_code": "CJU",
                            "arrival_airport_code": "GMP",
                            "seat_stock": 5
                        },
                        {
                            "id": 2,
                            "flight_id": 2,
                            "flight_number": "KA102",
                            "departure_datetime": "2021-07-03T08:05:00",
                            "arrival_datetime": "2021-07-03T09:15:00",
                            "duration": "01:10:00",
                            "price": "100000.00",
                            "departure_city_name": "제주",
                            "arrival_city_name": "서울/김포",
                            "departure_airport_code": "CJU",
                            "arrival_airport_code": "GMP",
                            "seat_stock": 5
                        }
                    ]
                }
            )
        self.assertEqual(response.status_code, 200)


