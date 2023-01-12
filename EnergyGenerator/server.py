# Create a multithreaded TCP server on the port entered as an input
# The server will listen for connections and create a new thread for each connection
# The thread will handle the connection and send the data to the client
# The server will also send the data to the client

import util.generateData as gd
import util.interfaceRequests as ir
import util.auction as au

import socket
import threading
import sys
import time
import json
from geopy import distance

PAUSE_TIME = 35  # 1800 30min normal (35s test)

# Create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = socket.gethostname()

# Get the port number from the user
try:
    port = int(sys.argv[1])
except:
    print("Please enter a port number")
    sys.exit()

print(f"Host: {host}:{port}")
# Bind to the port
serversocket.bind((host, port))

# Queue up to 5 requests
serversocket.listen(5)

# Create a new thread for each connection


def on_new_client(clientsocket, addr):
    global port
    global energy
    global pos
    global bids
    global soldState
    print("Got a connection from %s" % str(addr))
    price = -1
    while True:
        data = clientsocket.recv(1024)
        message = data.decode('utf-8')
        if message.startswith("PRICE"):
            ev = json.loads(f'{{{message.split("{")[1]}'.replace('\'', '\"'))
            dist = distance.geodesic(
                (ev['CarLat'], ev['CarLon']), (pos['lat'], pos['lon'])).km
            price = energy['basePrice'] + min(int(abs(dist)/2), 10)
            clientsocket.send(str(price).encode('utf-8'))
        if message.startswith("POS"):
            clientsocket.send(str(pos).encode('utf-8'))
        if message.startswith("ACCEPT") and soldState == False:
            # get Ev json
            print(f'{{{message.split("{")[1]}')
            ev = json.loads(f'{{{message.split("{")[1]}'.replace('\'', '\"'))
            # add bid to bids
            bids.append(ev)
            print(f'Number of bids : {len(bids)}')
            # create a bid on interface
            ir.sendBid(ev, price, port)
        if not data:
            break
        print("Received from client: %s" % data.decode('utf-8'))
    clientsocket.close()

# energy thread


def energyThread():
    global energy
    global pos
    global port
    global bids
    global soldState
    while True:
        # do the auction or/and create new energy every 30 min
        time.sleep(PAUSE_TIME)  # 1800 = 30 min (35s in test)
        if bids:
            # do the auction
            print('Auction in comming :')
            au.handleAuction(bids, energy, pos, port)
            soldState = True
            time.sleep(PAUSE_TIME)
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
    print(
        f'New Energy :\nBasePrice : {energy["basePrice"]}, CreatedTime: {energy["createdTime"]}')


pos = gd.generatePos()
print(f'Server pos : {pos["lat"]},{pos["lon"]}')

createEnergy()
soldState = False

# start thread for energy
threading.Thread(target=energyThread).start()

while True:
    # Establish a connection
    clientsocket, addr = serversocket.accept()
    # Create a new thread for each connection
    threading.Thread(target=on_new_client,
                     args=(clientsocket, addr)).start()
