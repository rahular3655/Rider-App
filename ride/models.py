from django.db import models
from accounts.models import User
from geopy.distance import great_circle


class StatusChoices(models.TextChoices):
        Requested =('requested', 'Requested'),
        Accepted = ('accepted', 'Accepted'),
        Completed = ('completed', 'Completed'),
        Cancelled = ('cancelled', 'Cancelled'),

class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=100)
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_color = models.CharField(max_length=100)

# Create your models here.
class Ride(models.Model):
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_requested')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_accepted', null=True, blank=True)
    pickup_location = models.PointField()
    dropoff_location = models.PointField()
    current_location = models.PointField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=StatusChoices.choices, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def distance(self, point1, point2):
        return great_circle((point1.y, point1.x), (point2.y, point2.x)).kilometers