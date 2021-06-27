import jwt

from django.test    import TestCase
from django.test    import Client

from unittest.mock  import patch, MagicMock
from users.models   import User

from welcome2air.settings import SECRET_KEY, ALGORITHM

class KakaoSignInTest(TestCase):
    def setUp(self):                        
        User.objects.create(
            id          = 1,
            kakao_id    = '1234567890',
            email       = 'jiupark@gmail.com',
            korean_name = '박지우'
        )

    def tearDown(self):                     
        User.objects.all().delete()

    @patch("users.views.requests")
    def test_kakao_login_exist_user_success(self, mocked_requests):  

        client = Client()                             

        class MockedResponse:                                             
            def json(self):
                return {                                                   
                            "id"            : "1234567890",
                            "kakao_account" : { 
                                "email"   : "jiupark@gmail.com",
                                'profile' : {'nickname' : '박지우'}
                            }
                        }

        mocked_requests.get = MagicMock(return_value = MockedResponse())

        headers             = {'HTTP_Authorization' : 'access_token'} 
        response            = client.get("/users", **headers)
        
        user         = User.objects.get(kakao_id='1234567890')
        access_token = jwt.encode({'user_id':1}, SECRET_KEY, ALGORITHM)

        self.assertEqual(response.json(),{'token':access_token})
        self.assertEqual(response.status_code, 200)