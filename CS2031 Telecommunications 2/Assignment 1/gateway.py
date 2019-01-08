#Made by: Marek Betka, 16324334

import socket
import sys
from _thread import start_new_thread

host = 'localhost'
port = 1000

hostList = ["main", "localhost:9999"]

#Setup for the socket module
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("Could not create socket")
    sys.exit()

#Bind the socket
try:
    s.bind((host, port))
except socket.error:
    print("Bind Failed.")
    sys.exit()

s.listen(10)
print("Listening...")

#Gateway funcion handles all incoming and outgoing packets after a connection has been established
def gateway(conn):
    #Gets name of server from the client, then looks through a list of server names to find a corresponding address to connect to
    try:
        data = conn.recv(4096)
        
        hostName = data.decode("UTF-8")
        try:
            ret = hostList.index(str(hostName))
            address = hostList[ret+1]
            host = address[:address.index(":")]
            port = int(address[address.index(":")+1:])
            print("Client has been connected to",address)
        except:
            conn.sendall(str.encode("Invalid server name!"))
            conn.close()
            return

        #Connects to server if one was found
        s = socket.socket()
        s.connect((host, port))
        conn.sendall(str.encode("Connected!"))
    except:
        print("An error occured!")
        conn.close()
        return
    
    s.settimeout(3)
    conn.settimeout(3)
    
    timesTimedOutServ = 0
    timesTimedOutClie = 0

    #Cycles through packets being exchanged, if a packet failed to send it times out and moves on.
    while True:
        #Recieve from client.
        try:
            data = conn.recv(4096)
            
            data = data.decode("UTF-8")
            s.sendall(str.encode(data))
            timesTimedOutClie = 0
        except:
            timesTimedOutClie+=1
            if (timesTimedOutClie == 10):
                s.close()
                conn.close()
                return
            
        #Recieve from server.
        try:
            servdata = s.recv(4096)
            
            servdata = servdata.decode("UTF-8")
            conn.sendall(str.encode(servdata))
            timesTimedOutServ = 0
        except:
            timesTimedOutServ+=1
            if (timesTimedOutServ == 10):
                s.close()
                conn.close()
                return
            
#Waits for a connection then creates a new thread for that connection.
while True:
    try:
        conn, addr = s.accept()
        print("Client " + addr[0] + ":" + str(addr[1]),"has connected to the gateway!")
    
        start_new_thread(gateway, (conn,))
    except:
        print("There was an error")
s.close()
