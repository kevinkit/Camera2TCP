# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:07:22 2017

@author: Kevin
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 20:52:38 2017

@author: kevin
"""

# Python TCP Client E
import socket
import numpy as np
import cv2
import binascii
import time
host = socket.gethostbyname(socket.gethostname())

port = 8080
BUFFER_SIZE = 305280
MESSAGE_ASK = "Connecting2SimpleImage"
MESSAGE = "SimpleImage"

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


print("BUFFER_SIZE " + str(BUFFER_SIZE))
_id = 0
while True:
    data = ''
    t0  = time.time()
    tcpClientA.send(MESSAGE)
    init = 0;
    try:
    	while len(data) < BUFFER_SIZE:
    		if init == 0:
    			data = tcpClientA.recv(BUFFER_SIZE)
    			init = 1;
    		else:
    			data += tcpClientA.recv(BUFFER_SIZE)

    except Exception:
        print("host unreachable...will try...forever...")
        continue;
    print (len(data))
#    print data
    print type(data)
    print data[len(data)-1]
    con = np.frombuffer(data,dtype=np.uint8)
    print con
    print con[len(con)-1]
 #   print np.frombuffer(data,dtype=np.uint8).tolist()
    img = np.frombuffer(data,dtype=np.uint8).reshape((int(shaping[0]),int(shaping[1]),int(shaping[2])))
#    img = np.frombuffer(data,dtype=np.uint8).reshape(193,10,3)
#    print img.tolist()
    t1 = time.time()
#    time.sleep(5)
#    if (t1 - t0) < 0.03:
#        time.sleep(1./30 - (t1 - t0))
#       # time.sleep(1)
#
#    if (float(t1) - float(t0)) < 1./30:
#        continue;
 #   cv2.imwrite('fu.png',img)
    cv2.imshow('something',img)
    _id = _id + 1;
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
tcpClientA.close()
