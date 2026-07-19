from django.contrib import admin
from .models import Event, TicketCategory

# Register your models here.

admin.site.register(Event)
admin.site.register(TicketCategory)
