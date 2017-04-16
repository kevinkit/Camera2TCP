# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 20:52:38 2017

@author: kevin
"""

# Python TCP Client A
import socket 
import numpy as np
import cv2
import binascii
host = socket.gethostbyname(socket.gethostname())
port = 8080
BUFFER_SIZE = 305280
MESSAGE = "RGB"
 
tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClientA.connect((host, port))
while True:
    tcpClientA.send(MESSAGE)    
    try:
        data = tcpClientA.recv(BUFFER_SIZE)
    except Exception:
        print("host unreachable...will try...forever...")
        continue;

    #Convert from ascii to string
    asstr = binascii.hexlify(data)
    #Split up after each byte couple
    n = 2
    split = [asstr[i:i+n] for i in range(0, len(asstr), n)]
    #Convert each byte couple to integer from its hex representation    
    asint = [];
    for i in split:    
        asint.append(int(i,16))   
        
    #Reshape into red,green and blue
    try:
        red = np.asarray(asint[::3]).reshape(240,424);
        green = np.asarray(asint[1::3]).reshape(240,424);
        blue = np.asarray(asint[2::3]).reshape(240,424);
    except ValueError:
        continue;
        
    #Reshape into an Image representation for opencv
    img = np.transpose(np.asarray([red,green,blue],dtype=np.uint8),axes=(1, 2, 0))

    #Show image
    cv2.imshow('something',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
tcpClientA.close() 
