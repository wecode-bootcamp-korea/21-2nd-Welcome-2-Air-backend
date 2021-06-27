from django.urls import path

from .views import TicketPdfView

urlpatterns = [
    path('/pdf', TicketPdfView.as_view()),
]