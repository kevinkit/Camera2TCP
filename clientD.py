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



import time
host = socket.gethostbyname(socket.gethostname())

port = 2004
BUFFER_SIZE = 305280
MESSAGE_ASK = "Connecting2KinectDepth"
MESSAGE = "Depth"
 
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
    print data      
    print shaping
    for i in range(0,len(shaping)):
        shaping[i] = int(shaping[i])
    BUFFER_SIZE =2*( int(shaping[0])*int(shaping[1])*int(shaping[2]))
   # BUFFER_SIZE = 434176
    break;


print("Buffer size: " + str(BUFFER_SIZE));


while True:
    print("trying")
    t0  = time.time()
    tcpClientA.send(MESSAGE) 
    print("message was send")
    
    try:
        print("waiting...")
        data = tcpClientA.recv(BUFFER_SIZE)
        print("recieving data")
    except Exception:
        print("host unreachable...will try...forever...")
        continue;
    print ("Recieved data len: " + str(len(data)))
    #print data
    if data != "no depth frame" and len(data) == BUFFER_SIZE:      
        temp = np.frombuffer(data,dtype=np.uint8)
        h = np.asarray(temp[0::2],dtype=np.uint16)
        l = np.asarray(temp[1::2],dtype=np.uint16)
        res = (h << 8) + l
        img = res.reshape(shaping[1],shaping[0])
        print(img.dtype)
        print(max(img[0]))
        #Sinec it is 12 bit
        rep = np.asarray(img >> 5,dtype=np.uint8)
    else:
        continue;


    cv2.imshow('something',rep)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
tcpClientA.close() 
