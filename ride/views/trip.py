from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, UpdateAPIView
from ride.models import Trip
from ride.serializers.trip import TripSerializer
from drf_spectacular.utils import extend_schema



@extend_schema(tags=["Trip"], summary="Trip Detail", request=TripSerializer)
class TripDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    lookup_field = 'id'  # Use 'id' as the lookup field for detail view

@extend_schema(tags=["Trip"], summary="Trip list", request=TripSerializer)
class TripListView(ListAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

@extend_schema(tags=["Trip"], summary="Trip update", request=TripSerializer)
class TripUpdateView(UpdateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer