# create a tcp client that will connect to the HOST at port 443

import util.generateData as gd

import socket
import sys

ev = gd.generateEv()

HOST = 'glenn-ubuntu'

# Get the port number from the user
try:
    port = int(sys.argv[1])
except:
    print("Please enter a port number")
    sys.exit()

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
s.connect((HOST, port))

# ask for Price to the server
s.sendall('PRICE'.encode('utf-8'))

# receive price from the server
data = s.recv(1024)

price = data.decode('utf-8')
print(f'Generator price is {price}')

# accepting
s.sendall(f'ACCEPT {ev}'.encode('utf-8'))

# close the connection
s.close()

print('Received', repr(data))
