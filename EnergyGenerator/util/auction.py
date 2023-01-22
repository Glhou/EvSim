# handle the auction function
import util.interfaceRequests as ir
import logging


def onlyOneGeneratorList(bids):
    return [b for b in bids if b['CarNbGenerator'] == 1]


def searchClosest(bids, pos):
    if not bids:
        return None
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


def lessEnergyBids(bids):
    if not bids:
        return None
    e_min = bids[0]['CarEnergy']
    lessEnergy = [bids[0]]
    for bid in bids:
        if bid['CarEnergy'] < e_min:
            e_min = bid['CarEnergy']
            lessEnergy = [bid]
        elif bid['CarEnergy'] == e_min:
            lessEnergy.append(bid)
    return lessEnergy


def handleAuction(bids, energy, pos):
    '''
    Parameters : distance, energy, number of generator available of a bid
    Here is the priority for the auction :
    1. The bid with only one generator available has priority but :
        a. If two or more bids are in this case you resolve with the remaining rules
        (b.) If was rejected by other generator and now has only one generator, can "No choice" and join the list of one generator (go for a. or 1. directly)
    2. The bid with the less energy
    3. The bid with the less distance
    '''
    winner = None
    logging.info(f"Bidders : {', '.join([b['CarId'] for b in bids])}")
    # 1. The bid with only one generator available has priority
    oneGeneratorList = onlyOneGeneratorList(bids)
    if oneGeneratorList:
        # 2. the bids with the less energy
        lessEnergyList = lessEnergyBids(oneGeneratorList)
        if len(lessEnergyList) == 1:
            return lessEnergyList[0]
        # 3. the bid with the less distance
        closest = searchClosest(lessEnergyList, pos)
        logging.info(f'Closest bid with only one generator : {closest}')
        winner = closest
        # send the winner
        return winner
    # 2. the bids with the less energy
    lessEnergyList = lessEnergyBids(bids)
    if len(lessEnergyList) == 1:
        return lessEnergyList[0]
    closest = searchClosest(lessEnergyList, pos)
    logging.info(f'Closest bid : {closest}')
    winner = closest
    # send the winner
    return winner
