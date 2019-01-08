#Made by: Marek Betka, 16324334

import socket
import random as rand
import time

def Client():
    address = str(input("Type in your ip:port or press enter to connect to gateway: "))
    serv = ""
    #Converts valid serverIp:port to variables if a valid serverIp:port is input.
    #If not, it connects to the gateway outlined in the spec.
    try:
        if address.index(":") != 0:
            host = address[:address.index(":")]
            port = int(address[address.index(":")+1:])
    except:
        serv = input("Which server would you like to connect to? Type 'main' for main server: ")
        #My gateway port and ip
        host = "localhost"
        port = 1000
    
    #Tries to connect to the gateway, binding is done automatically to an available port.
    s = socket.socket()
    try:
        s.connect((host, port))
    except:
        print("Failed to connect to gateway!")
        return
    #Relays name of server to gateway so it can find a server to connect to.

    if (serv != ""):
        serv = serv.encode("UTF-8")
        s.sendall(serv)

    #Setup variables for main loop
    message = ""
    lastmessage =4 
    timesTimedOut = 0
    smallError = 0
    s.settimeout(4)
    
    while True:
        try:
            message = str(lastmessage + 1)
            data = s.recv(4096)
            data = data.decode("UTF-8")
            print("Recieved:",data)
            if (message == "21"):
                break
            if (data[0:5] == "NACK:"):
                message = data[5:]
                lastmessage = int(data[5:])
                print("Resending:",message)
                message = message.encode("UTF-8")
                s.sendall(message)
            else:
                smallError = rand.randint(1,5)
                if (smallError != 1):
                    print("Sending:",message)
                    message = message.encode("UTF-8")
                    s.sendall(message)
                else:
                    print("Sending:",message,"(has failed)")
            
            lastmessage = int(message)

            timesTimedOut = 0
        #Exception if client failed to recieve data.
        except:
            print("Time out: Server did not respond")
            timesTimedOut+=1
            if (timesTimedOut == 5):
                break
    s.close()
    
#Runs the client code.
Client()
time.sleep(5)
