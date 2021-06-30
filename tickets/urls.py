from tickets.views import ReservationView
from django.urls import path

# from .views import FileView

urlpatterns=[
    # path('/pdfUpload', FileView.as_view())
    path('/reservation', ReservationView.as_view())
]