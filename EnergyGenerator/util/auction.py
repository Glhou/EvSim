# handle the auction function
import util.interfaceRequests as ir


def searchClosest(bids, pos):
    d_min = (bids[0]['CarLat'] - pos['lat'])**2 + \
        (bids[0]['CarLon'] - pos['lon'])
    closest = bids[0]
    for bid in bids:
        d = (bid['CarLat'] - pos['lat'])**2 + \
            (bid['CarLon'] - pos['lon'])**2
        if d < d_min**2:
            d_min = d
            closest = bid
    return closest


def handleAuction(bids, energy, pos, port):
    print(f"Bidders : {', '.join([b['CarId'] for b in bids])}")
    closest = searchClosest(bids, pos)
    print(f'Closest bid : {closest}')
    # send the winner to the closest
    ir.sendAuction(f"tok-{port}", closest['CarId'])
