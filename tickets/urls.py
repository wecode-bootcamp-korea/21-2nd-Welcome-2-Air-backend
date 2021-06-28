from django.urls   import path
from tickets.views import ReservationPost, ReservationSearch

urlpatterns = [
    path('/reservation', ReservationPost.as_view()),
    path('/search', ReservationSearch.as_view())
] 