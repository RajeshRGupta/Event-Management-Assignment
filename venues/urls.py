from django.urls import path
from .views import VenueListCreateView

urlpatterns = [
    path("", VenueListCreateView.as_view()),
]
