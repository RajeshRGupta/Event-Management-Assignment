from django.db import models
from accounts.models import User
from events.models import Event, TicketCategory
import uuid

class Booking(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Failed", "Failed"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_category = models.ForeignKey(TicketCategory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    ticket_code = models.CharField(max_length=100,blank=True,null=True)
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
    

class Payment(models.Model):
    STATUS_CHOICES = (
        ("Success", "Success"),
        ("Failed", "Failed"),
    )
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES)
    payment_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.transaction_id)