from django.urls import path

from .views import TicketPdfView, ReservationView

urlpatterns = [
    path('/pdf', TicketPdfView.as_view()),
    path('/reservation', ReservationView.as_view())
]