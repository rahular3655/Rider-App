from rest_framework import serializers
from ride.models import Ride
from accounts.models import User

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'
        
