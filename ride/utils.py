
from geopy.distance import great_circle
from ride.models import Driver

def calculate_distance(point1, point2):
    """
    Calculates the great-circle distance between two points in kilometers.
    Args:
        point1: A Point object representing the first location.
        point2: A Point object representing the second location.
    Returns:
        Distance in kilometers.
    """
    return great_circle((point1.y, point1.x), (point2.y, point2.x)).kilometers


def get_closest_driver(pick_up_location):
    """
    Finds the closest available driver to the pickup location.
    Args:
        pick_up_location: A Point object representing the pickup location.
    Returns:
        The closest Driver object or None if no available drivers are found.
    """
    drivers = Driver.objects.filter(is_available=True)
    shortest_distance = float('inf')
    closest_driver = None

    for driver in drivers:
        driver_location = driver.current_location
        distance = calculate_distance(driver_location, pick_up_location)
        if distance < shortest_distance:
            shortest_distance = distance
            closest_driver = driver

    return closest_driver