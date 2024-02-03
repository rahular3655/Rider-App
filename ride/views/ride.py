from rest_framework import generics
from ride.models import Ride
from rest_framework.authentication import TokenAuthentication
from ride.serializers.ride import RideSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Ride"], summary="Ride Create", request=RideSerializer)
class RideRequestCreateView(generics.CreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    authentication_classes = [TokenAuthentication]
    
@extend_schema(tags=["Ride"], summary="Ride detail", request=RideSerializer)
class RideDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    authentication_classes = [TokenAuthentication]

@extend_schema(tags=["Ride"], summary="Ride list", request=RideSerializer)
class RideListView(generics.ListAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    authentication_classes = [TokenAuthentication] 
    
@extend_schema(tags=["Ride"], summary="Ride update", request=RideSerializer)    
class RideUpdateView(generics.UpdateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    authentication_classes = [TokenAuthentication]