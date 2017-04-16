# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 18:59:08 2017

@author: kevin


Please see: 

http://stackoverflow.com/questions/23828264/how-to-make-a-simple-multithreaded-socket-server-in-python-that-remembers-client
"""

import socket
import threading

#Check every 10 Seconds if the thread should be dead
socket.setdefaulttimeout(10)


class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.comThreads = []
        self.alive = True;
    def listenWrapper(self,client,address):
        client, address = self.sock.accept()
    
    def listen(self):
        self.sock.listen(5)
        while True:
            try:
                client, address = self.sock.accept()
                client.settimeout(60)              
                threading.Thread(target = self.listenToClient,args = (client,address)).start()
            except socket.timeout:
                #self.sock.close()
                if self.alive:
                    continue;
                else:
#                    for t in self.comThreads:
#                        if t.isAlive():
#                            t.join(0.1)
                    break;

    def listenToClient(self, client, address):
        size = 1024
        while self.alive:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data 
                    response = data
                    client.send(response)
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

if __name__ == "__main__":
    #port_num = input("Port? ")
    print("I am on: " + socket.gethostbyname(socket.gethostname()))    
    port_num = 8080
    TS = ThreadedServer(socket.gethostbyname(socket.gethostname()),port_num)
    t = threading.Thread(target=TS.listen)
    t.start();
    while(1):
        try:
            print"hi"
        except KeyboardInterrupt:
            break;
    TS.sock.close();
    TS.alive = False;
    if t.isAlive():    
        print("closing...")
        t.join(0.1);
        print("closed...")
