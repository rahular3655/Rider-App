from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from ride.models import Driver
from ride.serializers.driver import DriverSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Driver"], summary="Driver Create", request=DriverSerializer)
class DriverCreateView(generics.CreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

@extend_schema(tags=["Driver"], summary="update", request=DriverSerializer)        
class DriverDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    lookup_field = 'id'