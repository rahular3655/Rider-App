import pytest
from .models import Trip,Ride
from geopy.point import Point


@pytest.mark.django_db
def test_create_ride():
    # Create a sample ride
    ride = Ride.objects.create(
        customer_id=1,
        pickup_point=Point(x=10.0, y=20.0),
        dropoff_point=Point(x=15.0, y=25.0),
        current_location=Point(x=12.0, y=22.0),
        status='Requested'
    )

    # Check if the ride was created successfully
    assert ride.id is not None

@pytest.mark.django_db
def test_ride_defaults():
    # Create a ride with default values
    ride = Ride.objects.create(customer_id=1)

    # Check default values
    assert ride.status == 'Requested'

@pytest.mark.django_db
def test_distance_calculation():
    # Create two points
    point1 = Point(x=10.0, y=20.0)
    point2 = Point(x=15.0, y=25.0)

    # Calculate distance
    distance_km = Ride.distance(point1, point2)

    # Check if distance calculation is correct
    assert distance_km == 618.0
    

@pytest.mark.django_db
def test_create_trip():
    # Create a sample trip
    trip = Trip.objects.create(
        ride_id=1,
        driver_id=2,
        is_active=True,
        status='Started'
    )

    # Check if the trip was created successfully
    assert trip.id is not None

@pytest.mark.django_db
def test_trip_defaults():
    # Create a trip with default values
    trip = Trip.objects.create(ride_id=1)

    # Check default values
    assert trip.is_active is True
    assert trip.status == 'Started'

@pytest.mark.django_db
def test_updated_at():
    # Create a trip
    trip = Trip.objects.create(ride_id=1)

    # Update the trip
    trip.is_active = False
    trip.save()

    # Check if updated_at field changed
    assert trip.updated_at != trip.created_at