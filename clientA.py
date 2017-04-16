# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 20:52:38 2017

@author: kevin
"""

# Python TCP Client A
import socket 
import numpy as np
import cv2
host = socket.gethostbyname(socket.gethostname())
port = 8080
BUFFER_SIZE = 2000 
MESSAGE = "RGB"
 
tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClientA.connect((host, port))
 
while True:
    tcpClientA.send(MESSAGE)     
    data = tcpClientA.recv(BUFFER_SIZE)
    #print " Client2 received data:", data
    #MESSAGE = raw_input("tcpClientA: Enter message to continue/ Enter exit:")
    print(data)    
    print(np.asarray(data).shape)
tcpClientA.close() 
