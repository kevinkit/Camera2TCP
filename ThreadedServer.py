# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 18:59:08 2017

@author: kevin


Please see: 

http://stackoverflow.com/questions/23828264/how-to-make-a-simple-multithreaded-socket-server-in-python-that-remembers-client
"""

import socket
import threading
import cv2
#Check every 10 Seconds if the thread should be dead
socket.setdefaulttimeout(10)


class ThreadedServer(object):
    def __init__(self, host, port,camtype="webcam",ID=0):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.comThreads = []
        self.alive = True;
        self.RGB0 = [];
        self.RGB1 = [];
        self.Depth = [];
        self.Body = [];
        self.camtype = camtype;
        self.lock0 = False;
        self.lock1 = True;
        self.ret = False;
        if camtype == "webcam":
            import cv2
            self.cap = cv2.VideoCapture(ID)
            
    def listenWrapper(self,client,address):
        client, address = self.sock.accept()
    def imageCapture(self):
        if self.camtype == "webcam":
            ret, frame = self.cap.read()
            if ret:
           #     #First container is locked
           #     if self.lock0:
                 self.RGB0 = frame;
                 self.ret = ret;
#                    self.lock0 = False;
#                else:
#                    self.RGB1 = frame;
#                    self.lock0 = True;
#                
        return ret
    def listen(self):
        self.sock.listen(5)
        while True:
            try:
                client, address = self.sock.accept()
                #self.imageCapture();
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
                    #response = data
                    #client.send(response)
                    #if data == 'RGB':
     #                   if self.lock0:
      #                      client.send(self.RGB1)
      #                  else:

                        client.send(self.RGB0)

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
            
            TS.imageCapture()
   #         if TS.lock0:
   #             print(len(TS.RGB1))
  #              print(TS.RGB1.shape)
                #cv2.imshow('frame',TS.RGB1)
  #          else:
            print(TS.RGB0.shape)
            
        #    if TS.ret:
        #        cv2.imshow('frame',TS.RGB0)
            
            
        except KeyboardInterrupt:
            break;
    TS.sock.close();
    TS.alive = False;
    if t.isAlive():    
        print("closing...")
        t.join(0.1);
        print("closed...")
