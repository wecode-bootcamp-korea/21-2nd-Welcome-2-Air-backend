from django.urls import path, include

urlpatterns = [
    path('flights', include('flights.urls'))
]