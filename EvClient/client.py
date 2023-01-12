# create a tcp client that will connect to the HOST at port 443

import util.generateData as gd
import util.distance as ds
import util.chooseGenerator as cg

import socket
import sys
import threading
import time
import json

ev = gd.generateEv()

HOST = 'glenn-ubuntu'

PAUSE_TIME = 35  # 1800 = 30min normal (35s test)

accepted = False
prices = []
generators = []

# Get the port number from the user
try:
    ports = sys.argv[1:]
except:
    print("Please enter a list of ports number (ex : python client.py 4442 4443 ...")
    sys.exit()


def handlePort(port):
    global accepted
    global generators
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the server
    s.connect((HOST, port))

    # ask for Price to the server
    s.send(f'PRICE {ev}'.encode('utf-8'))

    # receive price from the server
    price = int(s.recv(1024).decode('utf-8'))

    # ask for pos to the server
    s.send(f'POS {ev}'.encode('utf-8'))

    # receive pos from the server
    pos = json.loads(s.recv(1024).decode('utf-8').replace("'", '"'))
    # compute the distance in meter then put it in kilometers
    dist = int(ds.latlonDist(pos['lat'], pos['lon'],
                             ev['CarLat'], ev['CarLon']) / 1000)  # km
    print(f'Generator is {dist}km from the car')

    print(f'Generator price is {price}')

    generators.append({'port': port, 'price': price, 'dist': dist})

    # wait a bit
    time.sleep(1)

    # choose the generator in range with min price
    choosedPort = cg.choose(generators, ev['CarRadius'])

    # accepting if minimum price
    if port == choosedPort and not accepted:
        print(f'Accepting {port} offer for {price}')
        s.send(f'ACCEPT {ev}'.encode('utf-8'))
        accepted = True
        generators = []
        # wait 30min and set accepted to false (35s in test)
        time.sleep(PAUSE_TIME)
        accepted = False
    # close the connection
    s.close()


for port in ports:
    # create a thread for handle port
    threading.Thread(target=handlePort, args=(int(port),)).start()
