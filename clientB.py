# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 20:52:38 2017

@author: kevin

This is a simple client for getting HD-RGB data from the Kinect v2 

"""

# Python TCP Client A
import socket 
import numpy as np
import cv2
import binascii
import time
host = socket.gethostbyname(socket.gethostname())

port = 2004
BUFFER_SIZE = 305280
MESSAGE_ASK = "Connecting2KinectWebcam"
MESSAGE = "RGBHD"
 
tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClientA.connect((host, port))


#Send request
while True:
   
    try:
        print("trying on " + str(host))
        tcpClientA.send(MESSAGE_ASK);
        data = tcpClientA.recv(BUFFER_SIZE)
    except Exception:
        print data
        print("host unreachable...will...try..to..connect again");
        continue;

    shaping = data.split(',')
    print shaping

    for i in range(0,len(shaping)):
        shaping[i] = int(shaping[i])
    BUFFER_SIZE = int(shaping[0])*int(shaping[1])*int(shaping[2])
    break;


print("Buffer size: " + str(BUFFER_SIZE));
print("Shape:" + str(shaping))

while True:
    print("trying")
    t0  = time.time()
    tcpClientA.send(MESSAGE) 
    print("message was send")
    print shaping
    try:
        print("waiting...")
        data = tcpClientA.recv(BUFFER_SIZE)
        print("recieving data")
    except Exception:
        print("host unreachable...will try...forever...")
        continue;
    print ("Recieved data len: " + str(len(data)))
 #   print np.frombuffer(data,dtype=np.uint8)
 
    if data != "no frame":
        img = np.frombuffer(data,dtype=np.uint8).reshape((int(shaping[0]),int(shaping[1]),int(shaping[2])))
        t1 = time.time()
    
    print("FPS: " + str(1/(t1-t0)))
#    if (float(t1) - float(t0)) < 1./30:
#        continue;

    cv2.imshow('something',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
tcpClientA.close() 
