# create a tcp client that will connect to the HOST at port 443

import util.generateData as gd
import util.distance as ds
import util.chooseGenerator as cg
import util.data as dt

import socket
import sys
import threading
import time
import json
import logging
import requests
import atexit

logging.basicConfig(level=logging.WARNING)

ev = gd.generateEv()

HOST = 'glenn-ubuntu'

# set parameters form arguments
try:
    PAUSE_TIME = int(sys.argv[2])
except:
    PAUSE_TIME = 10

try:
    TIMEOUT = int(sys.argv[3])
except:
    TIMEOUT = 5

# If one of the generator in the X less pricy reply you are a winner you accept
try:
    NB_BEST_GENERATOR = int(sys.argv[4])
except:
    NB_BEST_GENERATOR = 2


acceptedEnergy = False
prices = []
generators = []
nbOfGenerators = 0  # number of generators that the client connected to
resultsQueue = []

# Get the port number from the user
try:
    ports = sys.argv[1].split(',')
except:
    logging.error(
        "Please enter a list of ports number (ex : python client.py 4442 4443 ...")
    sys.exit()


def handlePort(port):
    global acceptedEnergy
    global generators
    global nbOfGenerators
    global resultsQueue
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the server
    s.connect((HOST, port))

    # ask for pos to the server
    s.send(f'POS {ev}'.encode('utf-8'))

    # receive pos from the server
    pos = json.loads(s.recv(1024).decode('utf-8').replace("'", '"'))
    # compute the distance in meter then put it in kilometers
    dist = int(ds.latlonDist(pos['lat'], pos['lon'],
                             ev['CarLat'], ev['CarLon']) / 1000)  # km

    # add the nbOfGenerators if the generator is in range only, if not stop the connection
    if dist > ev['CarRadius']:
        s.close()
        return -1
    nbOfGenerators += 1
    ev["CarNbGenerator"] = nbOfGenerators

    # ask for Price to the server
    s.send(f'PRICE {ev}'.encode('utf-8'))

    # receive price from the server
    price = int(s.recv(1024).decode('utf-8'))

    if price > ev['CarMaxPrice']:
        s.close()
        return -1

    logging.info(f'Generator is {dist}km from the car')

    logging.info(f'Generator price is {price}')

    generators.append({'port': port, 'price': price, 'dist': dist})

    # wait a bit for other connections
    time.sleep(1)

    # get the X less pricy generators, if one reply we automatically say ok
    bestPorts = cg.chooseBestsPorts(
        generators, ev['CarRadius'], NB_BEST_GENERATOR)

    # accept all offer
    logging.info(f'Accepting {port} offer for {price}')
    s.send(f'ACCEPT {ev}'.encode('utf-8'))

    # wait until get Results of the auction from the Generators
    result = s.recv(1024).decode('utf-8')
    resultsQueue.append(result)

    start_process = time.time()

    # wait for the results to be first in the results queue
    while resultsQueue[0] != result:
        time.sleep(0.5)
        if time.time() - start_process > TIMEOUT*4:
            logging.info(f'Rejected the auction for {port}')
            s.send(f'NACK {ev}'.encode('utf-8'))
            resultsQueue.pop(0)
            s.close()
            return -1

    if result.startswith('WON') and not acceptedEnergy:
        if port in bestPorts and not acceptedEnergy:
            # instantly win
            acceptedEnergy = True
            logging.info(f'Won the auction for {port}')
            s.send(f'ACK {ev}'.encode('utf-8'))
        else:
            # wait for half timeout
            time.sleep(TIMEOUT / 2)
            if not acceptedEnergy:
                # if we didn't get any other offer, we accept the offer
                acceptedEnergy = True
                logging.info(f'Won the auction for {port}')
                s.send(f'ACK {ev}'.encode('utf-8'))
            else:
                # if we got an other offer, we reject the offer
                logging.info(f'Rejected the auction for {port}')
                s.send(f'NACK {ev}'.encode('utf-8'))

    # execution done so remove result from resultsQueue
    resultsQueue.pop(0)
    s.close()


start_time = time.time()

threads = []
for port in ports:
    # create a thread for handle port
    t = threading.Thread(target=handlePort, args=(int(port),))
    t.start()
    threads.append(t)

# wait for all the threads to finish
while any(t.is_alive() for t in threads):
    pass


def exitFun(generators, ev):
    if not generators:
        requests.post('http://localhost:8080/ev', json=ev)
        # wait PAUSE TIME
        time.sleep(PAUSE_TIME)
        ev['CarEnergy'] = -1
        requests.post('http://localhost:8080/ev', json=ev)


atexit.register(exitFun, generators, ev)  # icon at the end on the interface

# get datas
dt.connectionStatus(acceptedEnergy, start_time)
