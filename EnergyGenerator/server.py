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
    print("Got a connection from %s" % str(addr))
    while True:
        data = clientsocket.recv(1024)
        message = data.decode('utf-8')
        if message == "PRICE":
            clientsocket.send(str(energy['basePrice']).encode('utf-8'))
        if message.startswith("ACCEPT"):
            # get Ev json
            print(f'{{{message.split("{")[1]}')
            ev = json.loads(f'{{{message.split("{")[1]}'.replace('\'', '\"'))
            # add bid to bids
            bids.append(ev)
            print(f'Number of bids : {len(bids)}')
            # create a bid on interface
            ir.sendBid(ev, energy['basePrice'], port)
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
    while True:
        # do the auction or/and create new energy every 30 min
        time.sleep(35)  # 1800 = 30 min
        if bids:
            # do the auction
            print('Auction in comming :')
            au.handleAuction(bids, energy, pos, port)
        createEnergy()


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

# start thread for energy
threading.Thread(target=energyThread).start()

while True:
    # Establish a connection
    clientsocket, addr = serversocket.accept()
    # Create a new thread for each connection
    threading.Thread(target=on_new_client,
                     args=(clientsocket, addr)).start()