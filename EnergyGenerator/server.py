# Create a multithreaded TCP server on the port entered as an input
# The server will listen for connections and create a new thread for each connection
# The thread will handle the connection and send the data to the client
# The server will also send the data to the client

import util.generateData as gd
import util.interfaceRequests as ir
import util.auction as au
import util.data as dt

import socket
import threading
import sys
import time
import json
import logging
from geopy import distance

logging.basicConfig(level=logging.WARNING)


def on_new_client(clientsocket, addr):
    global port
    global energy
    global pos
    global bids
    global soldState
    global winner
    global winnerAck
    logging.info("Got a connection from %s" % str(addr))
    price = -1
    ev = {}
    auctionned = False
    while True:
        message = ""
        if not auctionned:
            # we want to get the message while we auction
            # this way we can check for the winner
            data = clientsocket.recv(1024)
            message = data.decode('utf-8')
        if message.startswith("POS"):
            logging.debug('Asked for POS')
            clientsocket.send(str(pos).encode('utf-8'))
        if message.startswith("PRICE"):
            logging.debug('Asked for PRICE')
            # get the ev
            ev = json.loads(f'{{{message.split("{")[1]}'.replace('\'', '\"'))
            dist = distance.geodesic(
                (ev['CarLat'], ev['CarLon']), (pos['lat'], pos['lon'])).km
            price = energy['basePrice'] + min(int(abs(dist)/2), 10)
            clientsocket.send(str(price).encode('utf-8'))
        if message.startswith("ACCEPT") and soldState == False:
            logging.debug('Client ACCEPT')
            # get Ev json
            logging.debug(f'{{{message.split("{")[1]}')
            ev = json.loads(f'{{{message.split("{")[1]}'.replace('\'', '\"'))
            # add bid to bids
            bids.append(ev)
            logging.info(f'Number of bids : {len(bids)}')
            # create a bid on interface
            ir.sendBid(ev, price, port)
            auctionned = True
        if winner == ev and not winnerAck and auctionned:
            logging.debug(f'Winning client is beeing contacted')
            # ask the client if accept the energy
            clientsocket.send("WON".encode('utf-8'))
            # wait for the client to reply
            data = clientsocket.recv(1024)
            logging.debug(f'Winning client has replied')
            if data.decode('utf-8').startswith("ACK"):
                winnerAck = True
                logging.info('Auction won')
                clientsocket.close()
            elif data.decode('utf-8').startswith('NACK'):
                winnerAck = False
                logging.info('Auction lost')
                clientsocket.close()
        if winnerAck and auctionned:
            logging.debug('Client has lost')
            try:
                clientsocket.send("LOST".encode('utf-8'))
            except:
                pass
    clientsocket.close()

# energy thread


def energyThread(pauseTime, timeout):
    global energy
    global pos
    global port
    global bids
    global soldState
    global winner
    global winnerAck
    while True:
        # do the auction or/and create new energy every 30 min
        time.sleep(pauseTime)  # 1800 = 30 min (35s in test)
        if bids:
            dt.numberOfBidsAtAuction(bids)
            # do the auction
            logging.info('Auction in comming :')
            winnerAck = False
            while not winnerAck and bids:
                winner = au.handleAuction(bids, energy, pos)
                # send a message to the winner in the on_new_client thread
                time.sleep(timeout)  # timeout for client to reply
                if not winnerAck:
                    bids.remove(winner)  # we remove the winner and change it
                    winner = None
            if winner:
                logging.info(f'Winner is {winner}')
                ir.sendAuction(f"tok-{port}", winner['CarId'])
                soldState = True
                time.sleep(pauseTime)
        createEnergy()
        soldState = False


def createEnergy():
    global pos
    global port
    global energy
    global bids
    bids = []  # reset all the bids
    energy = gd.generateEnergy()
    ir.sendEnergy(pos, energy, port)
    logging.info(
        f'New Energy :\nBasePrice : {energy["basePrice"]}, CreatedTime: {energy["createdTime"]}')


def server(port, pauseTime, timeout):
    global pos
    global port
    global energy
    global bids
    global soldState
    global winner
    global winnerAck

    # Create a socket object
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Get local machine name
    host = socket.gethostname()

    logging.info(f"Host: {host}:{port}")
    # Bind to the port
    serversocket.bind((host, port))

    # Queue up to 5 requests
    serversocket.listen(5)

    # Create a new thread for each connection

    pos = gd.generatePos()
    logging.info(f'Server pos : {pos["lat"]},{pos["lon"]}')

    createEnergy()
    soldState = False
    winner = None
    winnerAck = False

    # start thread for energy
    threading.Thread(target=energyThread, args=(pauseTime, timeout,)).start()

    while True:
        # Establish a connection
        clientsocket, addr = serversocket.accept()
        # Create a new thread for each connection
        threading.Thread(target=on_new_client,
                         args=(clientsocket, addr)).start()


if __name__ == "__main__":
    # set parameters form arguments
    try:
        pauseTime = int(sys.argv[2])
    except:
        pauseTime = 10  # 1800 30min normal (35s test)

    try:
        timeout = int(sys.argv[3])
    except:
        timeout = 5

    # Get the port number from the user
    try:
        port = int(sys.argv[1])
    except:
        logging.error("Please enter a port number")
        sys.exit()

    server(port, pauseTime, timeout)
