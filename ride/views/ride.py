from rest_framework import generics
from ride.models import Ride
from ride.serializers.ride import RideSerializer

class RideCreateView(generics.CreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

class RideDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

class RideListView(generics.ListAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer 
    
class RideUpdateView(generics.UpdateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer