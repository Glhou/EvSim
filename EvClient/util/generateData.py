# generate id pos and an energy percentage

import random
import hashlib


def generateEv():
    lat = random.uniform(35.2, 35.6)
    lon = random.uniform(139.5, 139.8)
    hashName = hashlib.sha256(f'{lat}:{lon}'.encode()).hexdigest()
    idName = f'Ev-{hashName}'
    energy = random.randint(0, 100)
    radius = 10 * energy / 100
    maxPrice = random.uniform(5, 20)
    return {
        "CarId": idName,
        "CarEnergy": energy,
        "CarRadius": radius,
        "CarLat": lat,
        "CarLon": lon,
        "CarMaxPrice": maxPrice,
    }
