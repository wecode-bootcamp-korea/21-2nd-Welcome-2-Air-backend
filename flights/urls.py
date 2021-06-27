from django.urls import path

from .views import FlightCountryListView, FlightListView

urlpatterns = [
    path('/country', FlightCountryListView.as_view()),
    path('',FlightListView.as_view())
]
