import math
from geopy import distance


def latlonDist(lat1, lon1, lat2, lon2):
    return distance.geodesic((lat1, lon1), (lat2, lon2)).meters
