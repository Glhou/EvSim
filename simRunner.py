import os
import threading
import time
import random
import requests
import subprocess
from multiprocessing import Manager
import sys

# check if data/connectionStatus.csv and data/numberOfBids.csv exists delete it if True
if os.path.exists('data/connectionStatus.csv'):
    os.remove('data/connectionStatus.csv')
if os.path.exists('data/numberOfBids.csv'):
    os.remove('data/numberOfBids.csv')

requests.get("http://127.0.0.1:8080/reset")  # reset the Interface on launch

# set parameters
nbMinClient = 5
nbMaxClient = 10
nbServer = 5

PAUSE_TIME = 30
TIMEOUT = 10
NB_BEST_GENERATOR = 2

CAR_GENERATION = [20, 30]  # min max

runTime = int(time.time() + 180)  # seconds

ports = [4010 + i for i in range(nbServer)]


def handleTimeoutProcess(client_process_timeout):
    for (p, start_time) in client_process_timeout:
        # if a client process lives longer than the time of an auction it must die
        if int(time.time()) - start_time > PAUSE_TIME*2:
            p.terminate()
            client_process_timeout.remove((p, start_time))


servers_process = []
# create a thread for each server
for port in ports:
    with open(f'data/logs/reportServer{port}.log', 'w') as f:
        p = subprocess.Popen(
            ["python3", "EnergyGenerator/server.py", f'{port}', f'{PAUSE_TIME}', f'{TIMEOUT}'], stdout=f, stderr=f)
        servers_process.append(p)


time.sleep(0.2)  # server startup

client_process = []
client_process_timeout = []
while runTime - int(time.time()) > 0:
    # create random 3-10 threads for the client
    for i in range(random.randint(nbMaxClient, nbMaxClient)):
        with open(f"data/logs/reportClient{len(client_process)}.log", 'w') as f:
            p = subprocess.Popen(
                ["python3", "EvClient/client.py", f"{','.join([str(p) for p in ports])}", f"{PAUSE_TIME}", f"{TIMEOUT}", f"{NB_BEST_GENERATOR}"], stdout=f, stderr=f)
            client_process.append(p)
            client_process_timeout.append((p, int(time.time())))
    time.sleep(random.randint(CAR_GENERATION[0], CAR_GENERATION[1]))
    print(
        f"Time remaining: {runTime - int(time.time())}, number of client: {len(client_process_timeout)}")
    # handleTimeoutProcess(client_process_timeout)


# kill the remaining process
for p in servers_process:
    p.terminate()

for p in client_process:
    p.terminate()
