from django.urls import path
from .views import KakaoSignIn

urlpatterns = [
   path('/login',KakaoSignIn.as_view()),
]