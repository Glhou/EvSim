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
    '''
    Parameters : distance, energy, number of generator available of a bid
    Here is the priority for the auction :
    1. The bid with only one generator available has priority but :
        a. If two or more bids are in this case you resolve with the remaining rules
        b. If was rejected by other generator and now has only one generator, can "No choice" and join the list of one generator (go for a. or 1. directly)
    2. The bid with the less energy
    3. The bid with the less distance
    '''
    print(f"Bidders : {', '.join([b['CarId'] for b in bids])}")
    closest = searchClosest(bids, pos)
    print(f'Closest bid : {closest}')
    # send the winner to the closest
    ir.sendAuction(f"tok-{port}", closest['CarId'])
