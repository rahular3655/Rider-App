from django.db import models
from accounts.models import User
from geopy.point import Point
from geopy.distance import great_circle
from django_lifecycle import hook, LifecycleModelMixin, AFTER_CREATE,AFTER_UPDATE


class StatusChoices(models.TextChoices):
        Requested =('requested', 'Requested')
        Accepted = ('accepted', 'Accepted')
        Completed = ('completed', 'Completed')
        Cancelled = ('cancelled', 'Cancelled')
        
class VehicleChoices(models.TextChoices):
        bike =('bike', 'Bike')
        scooter = ('scooter', 'Scooter')
        car = ('car', 'Car')
        
class TripStatusChoices(models.TextChoices):
        Started = ('started', 'Started')
        Ended = ('ended', 'Ended')
        Cancelled = ('cancelled', 'Cancelled')

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=100,choices=VehicleChoices.choices, blank=True, null=True)
    vehicle_number = models.CharField(max_length = 100,null=True,blank=True)
    current_location = Point()
    is_available = models.BooleanField(default=True)
    is_verified = models.BooleanField(default = True)
    
    @staticmethod
    def is_driver_available(driver_id):
        """
        Checks if the driver with the given ID is available.
        Args:
            driver_id: ID of the driver.
        Returns:
            True if the driver is available, False otherwise.
        """
        try:
            driver = Driver.objects.get(id=driver_id)
            return driver.is_available
        except Driver.DoesNotExist:
            return False
         

# Create your models here.
class Ride(LifecycleModelMixin,models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rides_requested')
    pickup_point = Point()
    dropoff_point = Point()
    current_location = Point()
    status = models.CharField(max_length=100, choices=StatusChoices.choices, blank=True, null=True,default = "Requested")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @staticmethod
    def distance(point1, point2):
        """
        Calculates the great-circle distance between two points in kilometers.
        Args:
            point1: A Point object representing the first location.
            point2: A Point object representing the second location.
        Returns:
            Distance in kilometers.
        """
        return great_circle((point1.y, point1.x), (point2.y, point2.x)).kilometers
    
    
    @hook(AFTER_CREATE, when='status', has_changed=True,was="Requested", priority=2)
    def create_trip(self):
        pick_up_location = self.pickup_point
        drivers = Driver.objects.filter(is_available=True)
        shortest_distance = float('inf')
        closest_driver = None

        for driver in drivers:
            driver_location = driver.current_location
            distance = self.distance(driver_location, pick_up_location)
            if distance < shortest_distance:
                shortest_distance = distance
                closest_driver = driver

        if closest_driver:
            Trip.objects.create(ride=self, driver=closest_driver)
        else:
            raise Exception("No available drivers found.")
    
    
class Trip(models.Model):
    ride = models.ForeignKey(Ride,on_delete=models.CASCADE, related_name='trip')  
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='trip_driver', null=True, blank=True)
    is_active =models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100, choices=TripStatusChoices.choices, blank=True, null=True,default = "Started")
    