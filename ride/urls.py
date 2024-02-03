from django.urls import path
from .views import driver,ride,trip

app_name = "ride"

urlpatterns = [
    path('drivers/', driver.DriverCreateView.as_view(), name='create-driver'),
    path('drivers/<int:id>/', driver.DriverDetailView.as_view(), name='driver-detail'),
    
    path('rides/create/', ride.RideRequestCreateView.as_view(), name='create-ride'),
    path('rides/<int:pk>/', ride.RideDetailView.as_view(), name='ride-detail'),
    path('rides/', ride.RideListView.as_view(), name='ride-list'),
    path('rides/<int:pk>/update/', ride.RideUpdateView.as_view(), name='update-ride'),
    
    path('trips/<int:id>/', trip.TripDetailView.as_view(), name='trip-detail'),
    path('trips/', trip.TripListView.as_view(), name='trip-list'),
    path('trips/<int:id>/update/', trip.TripUpdateView.as_view(), name='update-trip'),
]
