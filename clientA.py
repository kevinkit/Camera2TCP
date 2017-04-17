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
    
    img = np.frombuffer(data,dtype=np.uint8).reshape(240,424,3)

    cv2.imshow('something',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
tcpClientA.close() 
