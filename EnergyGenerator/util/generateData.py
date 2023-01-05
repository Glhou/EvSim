# generate a random coordonates in Yokohama

import random
import sys
import time


def generatePos():
    lat = random.uniform(35.2, 35.6)
    lon = random.uniform(139.5, 139.8)
    return {"lat": lat, "lon": lon}


def generateEnergy():
    # create a token of energy : {basePrice, createdTime,amount}
    basePrice = random.randint(1, 10)
    createdTime = time.time()
    return {"basePrice": basePrice, "createdTime": createdTime}
