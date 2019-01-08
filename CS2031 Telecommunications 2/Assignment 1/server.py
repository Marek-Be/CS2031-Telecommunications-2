#Made by: Marek Betka, 16324334

import socket
import sys
import random as rand
from _thread import start_new_thread

host = 'localhost'
port = 9999

#Setup for the socket module
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("Could not create socket. Error Code: ", str(msg[0]), "Error: ", msg[1])
    sys.exit(0)

#Bind the socket
try:
    s.bind((host, port))
except socket.error:
    print("Bind Failed.")
    sys.exit()
    
s.listen(10)
print("Listening...")

#Thread for each client that connects to the server.
def client_thread(conn):
    conn.settimeout(4)
    lastdata = -1
    timesTimedOut = 0
    seqNum = 0
    actualData = "";
    while True:
        try:
            data = conn.recv(4096)
            data = data.decode("UTF-8")
            print("Recieved:",data)
            #Functionality seperates the data from the sequence number using a ":"
            try:
                delimiter = data[::-1].index(":");
                seqNum = int(data[0:len(data)-delimiter])
                actualData = data[len(data)-delimiter:]
            except:
                seqNum = int(data)
            if (int(seqNum) == (lastdata+1)):
                
                reply = "ACK:" + data
                smallError = rand.randint(1,5)
                if (smallError != 1):
                    print("Sending:",reply)
                    conn.sendall(str.encode(reply))
                    lastdata = int(data)
                else:
                    print("Sending:",reply,"(has failed)")
                    lastdata = int(data)
            if (int(data) == 20):
                break
            
            timesTimedOut = 0
        #Exception if server failed to receive data, tries to correct the error.
        except:
            print("There was an error with the connection!")
            reply = "NACK:" + str(lastdata +1)
            conn.sendall(str.encode(reply))
            print("Sending:",reply)

            #Times timed out, if the server has failed to recieve anything
            #from the client, it will close the connection and end the thread.
            
            timesTimedOut+=1
            if (timesTimedOut == 5):
                conn.close()
                return

#Waits for a connection then creates a new thread for that connection.
while True:
    try:
        conn, addr = s.accept()
        print(addr[0] + ":" + str(addr[1]),"has connected to the server")
    
        start_new_thread(client_thread, (conn,))
    except:
        print("There was an error")
s.close()
