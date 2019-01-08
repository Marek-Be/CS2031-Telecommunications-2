#Made by: Marek Betka, 16324334

import socket
import sys
from _thread import start_new_thread

#List of routers with their associated connections.
R1=[10001,10003,100,10005,500,10101,100]
R2=[10002,10006,100]
R3=[10003,10001,100,10006,200,10008,200]
R4=[10004,10006,100,10007,50,10100,200]
R5=[10005,10001,500,10006,25,10007,25]
R6=[10006,10002,100,10003,200,10004,100]
R7=[10007,10004,50,10005,25,10008,100]
R8=[10008,10003,200,10007,100]
routingTable = [R1,R2,R3,R4,R5,R6,R7,R8]

controller_address = ('localhost',1050)

def Make_Router(port):
    #List of packets that are being held while controller finds shortest Path
    sentToController = []
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    routing_table = routingTable[port-1]
    router_address = ('localhost', 10000 + port)
    sock.bind(router_address)
    while True:
        print('\n'+str(10000+port)+ 'waiting to receive message')
        data, address = sock.recvfrom(4096)
        if data:
            message = data.decode("utf-8")
            print('\n'+str(10000+port) + "got data:" + message)
            #Flag handling
            if (message[0] == "s"):
                target = message.split(",")[0]
                lenTarget = len(target)
                
                sentToController.append(target.split(":")[1])
                sentToController.append(message[lenTarget:])

                target = target.encode()
                sent = sock.sendto(target, controller_address)
            elif (message[0] == "a"):
                
                fromRouter = message[1:].split(":")[0]
                
                if (fromRouter in sentToController):
                    routePath = message[1:].split(":")
                    sendToRouter = ('localhost',int(routePath[routePath.index(str(10000+port))+1]))

                    routeData = "d:"
                    pathString = ""
                    routePath = routePath[routePath.index(str(10000+port))+2:]
                    for each in routePath:
                        pathString += each + ":"
                    pathString = pathString[:-2]
                    routeData += pathString
                    routeData += sentToController[sentToController.index(fromRouter)+1]
                    sentToController = [];
                    routeData = routeData.encode("UTF-8")
                    sock.sendto(routeData,sendToRouter)
            elif (message[0] == "d"):
                routePath = message[1:].split(",")[0]
                routePath = routePath.split(":")
                
                sendToRouter = ('localhost',int(routePath[1]))

                message = message.replace(":" + routePath[1],"",1)

                message = message.encode("utf-8")
                sock.sendto(message,sendToRouter)

#Making each router
start_new_thread(Make_Router, (1,))
start_new_thread(Make_Router, (2,))
start_new_thread(Make_Router, (3,))
start_new_thread(Make_Router, (4,))
start_new_thread(Make_Router, (5,))
start_new_thread(Make_Router, (6,))
start_new_thread(Make_Router, (7,))
start_new_thread(Make_Router, (8,))
