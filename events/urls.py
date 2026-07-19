from django.urls import path
from .views import EventDetailView, EventListCreateView, TicketCategoryView

urlpatterns = [
    path("", EventListCreateView.as_view()),
    path("<int:id>/", EventDetailView.as_view()),
    path("tickets/", TicketCategoryView.as_view()),
]