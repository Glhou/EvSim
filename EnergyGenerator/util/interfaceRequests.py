import requests

HOST = "localhost"
PORT = 8080


def sendEnergy(pos, energy, port):
    requests.post(f'http://{HOST}:{PORT}/token', json={
        "TokenId": f"tok-{port}",
        "TokenLat": pos["lat"],
        "TokenLon": pos["lon"],
        "TokenPrice": energy["basePrice"],
    })


def sendBid(ev, price, port):
    requests.post(f'http://{HOST}:{PORT}/bid', json={
        "CarId": ev["CarId"],
        "CarEnergy": ev["CarEnergy"],
        "CarRadius": ev["CarRadius"],
        "CarLat": ev["CarLat"],
        "CarLon": ev["CarLon"],
        "Price": price,
        "TokenId": f"tok-{port}"
    })


def sendAuction(energyId, evId):
    requests.post(f'http://{HOST}:{PORT}/auction', json={
        "WinnerCarId": evId,
        "TokenId": energyId
    })
