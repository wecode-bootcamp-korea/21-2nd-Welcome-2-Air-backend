from django.urls import path, include

urlpatterns = [
    path('tickets', include('ticket.urls')),
    path('flights', include('flights.urls'))
]
