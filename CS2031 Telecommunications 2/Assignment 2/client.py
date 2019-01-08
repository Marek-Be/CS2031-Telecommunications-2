#Made by: Marek Betka, 16324334

import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_address = ('localhost', 10101)
print('starting up on {} port {}'.format(*client_address))
sock.bind(client_address)

server_address = ('localhost', 10100)
router_address = ('localhost', 10001)

while True:
    try:
        inputMessage = input("Enter what you want to send to the server:")
        message = "s"+client_address[0]+":"+str(client_address[1])+":"+server_address[0] + ":" + str(server_address[1]) + "," + inputMessage
        message = message.encode()
        # Send data
        print('sending {!r}'.format(message))
        sent = sock.sendto(message, router_address)

    except:
        print('closing socket')
        sock.close()
