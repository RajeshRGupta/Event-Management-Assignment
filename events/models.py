from django.db import models
from accounts.models import User
from venues.models import Venue


class Event(models.Model):
    organizer = models.ForeignKey(User,on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    def __str__(self):
        return self.title
    
    
class TicketCategory(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    total_quantity = models.IntegerField()
    available_quantity = models.IntegerField()
    def __str__(self):
        return self.name