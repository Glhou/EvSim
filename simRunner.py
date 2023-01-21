import os
import threading
import time
import random
import requests


requests.get("http://127.0.0.1:8080/reset")  # reset the Interface on launch

nbMinClient = 5
nbMaxClient = 10
nbServer = 10

ports = [4010 + i for i in range(nbServer)]


def handleServer(port):
    # exec the server with the port
    os.system(f"python3 EnergyGenerator/server.py {port}")


def handleClient():
    # exec the client sending all the ports
    os.system(
        f"python3 EvClient/client.py {' '.join([str(p) for p in ports])}")


# create a thread for each server
for port in ports:
    t = threading.Thread(target=handleServer, args=(port,))
    t.start()

while True:
    # create random 3-10 threads for the client
    for i in range(random.randint(nbMaxClient, nbMaxClient)):
        t = threading.Thread(target=handleClient)
        t.start()

    # wait btw 5 and 30 min (for test 5-35s)
    time.sleep(random.randint(5, 10))
