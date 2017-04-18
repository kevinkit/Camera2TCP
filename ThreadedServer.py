# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 18:59:08 2017

@author: kevin


Please see: 

http://stackoverflow.com/questions/23828264/how-to-make-a-simple-multithreaded-socket-server-in-python-that-remembers-client
"""

import socket
import threading
import sys
missings = 0


try:
    import cv2
except ImportError:
    print("Missing OpenCV!")
    missings = 1
#Advanced in case that Kinect is installed
try:
    from pykinect2 import PyKinectV2
    from pykinect2.PyKinectV2 import *
    from pykinect2 import PyKinectRuntime
    import ctypes
    import _ctypes
    import pygame
    import sys
except ImportError:
    print("Missing libs for Kinet!")
    if missings == 1:
        print("No library for camera detection found, neither OpenCV nor Kinect")
        sys.exit()


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
        self.log = "test"
        
        self.camids = [];
                      
        if camtype == "webcam":
            import cv2
            self.cap = cv2.VideoCapture(ID)
            
    def listenWrapper(self,client,address):
        client, address = self.sock.accept()
    def imageCapture(self):
        if self.camtype == "webcam":
            ret, frame = self.cap.read()
            self.ret = ret;
            if ret:
                 self.RGB0 = frame;       
                 return ret,frame
            else:
                 return ret, None
    def listen(self):
        self.sock.listen(5)
        while True:
            try:
                client, address = self.sock.accept()
                client.settimeout(60)              
                threading.Thread(target = self.listenToClient,args = (client,address)).start()
            except socket.timeout:
                if self.alive:
                    continue;
                else:
                    break;

    def listenToClient(self, client, address):
        size = 1024
        while self.alive:
            try:
                data = client.recv(size)
                self.log = data;
                if data:
                    #Send specific frame stuff
                    if data == "Connecting2RGBWebcam":   
                        self.log = "capturing"
                        re,frame = self.imageCapture()
                        if re:
                             self.log = "succesful init capture"
                             client.send(str(int(self.RGB0.shape[0])) + ',' + str(int(self.RGB0.shape[1]))+ ',' + str(int(self.RGB0.shape[2])))
                        else:
                             print("no service available")
                             self.log = "unsuccesful capture"
                             client.send("no service available")
                        #self.ret = False;
                    elif data == "RGB":
                        re,frame = self.imageCapture()
                        if re:
                            client.send(self.RGB0)
                            self.log  = "succesful loop capture"
                        else:
                            self.log = "unsuccesful loop capture"
                        #self.ret = False;
    
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

if __name__ == "__main__":
    print("I am on: " + socket.gethostbyname(socket.gethostname()))    
    port_num = 2004
    TS = ThreadedServer(socket.gethostbyname(socket.gethostname()),port_num)
    t = threading.Thread(target=TS.listen)
    t.start();

    while(1):
        try:
            print("I am on: " + socket.gethostbyname(socket.gethostname())) 

            
            if TS.ret:
                print(TS.RGB0.shape)
                print(TS.RGB0.size)
                print TS.log

                cv2.imshow('Server',TS.RGB0)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print("no cam detected!")
                print TS.log
        except KeyboardInterrupt:
            break;
            
    #Clean up 
    TS.sock.close();
    TS.alive = False;
    if t.isAlive():    
        print("closing...")
        t.join(0.1);
        print("closed...")
