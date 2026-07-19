from django.urls import path
from .views import BookingView, OrganizerBookingView, PaymentView

urlpatterns = [
    path("", BookingView.as_view()),
    path("payment/", PaymentView.as_view()),
    path("organizer/", OrganizerBookingView.as_view()),
]