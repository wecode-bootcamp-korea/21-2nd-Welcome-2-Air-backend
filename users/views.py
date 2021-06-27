from django.http      import JsonResponse
from django.views     import View

from users.models import User
from my_settings  import ALGORITHM, SECRET_KEY

import requests, jwt

class KakaoSignIn(View):
    def get(self, request):
            access_token    = request.headers.get('Authorization')
            profile_request = requests.get(
                "https://kapi.kakao.com/v2/user/me", headers={"Authorization":f"Bearer {access_token}"},
            )
        
            profile_json  = profile_request.json()
            kakao_account = profile_json["kakao_account"]
            email         = kakao_account["email"]
            kakao_id      = profile_json["id"]
            nick_name     = kakao_account["profile"]["nickname"]

            if User.objects.filter(kakao_id = kakao_id).exists():
                user = User.objects.get(kakao_id=kakao_id)
                token = jwt.encode({"user_id":user.id}, SECRET_KEY, ALGORITHM)
                return JsonResponse({"token": token},status = 200)

            else:
                User.objects.create(kakao_id = kakao_id, email = email, korean_name=nick_name)
                user = User.objects.get(kakao_id=kakao_id)
                token = jwt.encode({"user_id":user.kakao_id},SECRET_KEY, ALGORITHM)
                
                return JsonResponse({"token":token},status=200)

