# handle the auction function
import util.interfaceRequests as ir


def searchClosest(bids, pos):
    d_min = abs(bids[0]['CarLat'] - pos['lat']) + \
        abs(bids[0]['CarLon'] - pos['lon'])
    closest = bids[0]
    for bid in bids:
        d = abs(bid['CarLat'] - pos['lat']) + \
            abs(bid['CarLon'] - pos['lon'])
        if d < d_min:
            d_min = d
            closest = bid
    return closest


def handleAuction(bids, energy, pos, port):
    print(f"Bidders : {', '.join([b['CarId'] for b in bids])}")
    closest = searchClosest(bids, pos)
    print(f'Closest bid : {closest}')
    # send the winner to the closest
    ir.sendAuction(f"tok-{port}", closest['CarId'])
