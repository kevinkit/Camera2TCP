# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 12:10:39 2017

@author: Kevin
"""

#General classs for Connecting to any kind of Service
import socket
import numpy as np


class Client(object):
    def __init__(self,ConnectionType='SimpleImage',show=False,write=False,IP=socket.gethostbyname(socket.gethostname()),Port=8080, camId = 0):
        self.connectionType = ConnectionType;
        self.host = IP
        self.show = show;
        self.write = write;
        self.port = Port;
        self.camId = camId;
        self.BUFFER_SIZE = 305280
        self.MESSAGE_ASK = 'Connecting2' + ConnectionType
        self.MESSAGE = ConnectionType
        self.tcpClient = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.tcpClient.connect((IP,Port));        
        self.data = []
        self.shaping = []     
        self.data = ''
        self.img = []
    #Initialize connection
    def initConnection(self):
        while True:
          #  try:
                try:
                    print("Trying on" + str(self.host) + "with request" + self.MESSAGE_ASK)
                    self.tcpClient.send(self.MESSAGE_ASK);
                    self.data += self.tcpClient.recv(self.BUFFER_SIZE)
                except Exception as e:
                    print(e)
                    print("host unreachable, ...will...try...forever")
                    continue;

                if self.data == '':
                    print("invalid information")
                    continue
                
            
                self.shaping = self.data.split(',');
                if len(self.shaping) < 3:
                    print('invalid image size')
                    print(self.shaping)
                    return None;
                else:
                    for i in range(0,len(self.shaping)):
                        self.shaping[i] = int(self.shaping[i])
                    if self.connectionType != 'KinectDepth':                        
                        self.BUFFER_SIZE = int(self.shaping[0])*int(self.shaping[1])*int(self.shaping[2])
                    else:
                        self.BUFFER_SIZE = 2*int(self.shaping[0])*int(self.shaping[1])*int(self.shaping[2])
                return not None;
       #     except KeyboardInterrupt:
        ##        return None;                
        #        break;    
        
    def initConnection2(self):
        while True:
            try:
                print("trying on " + str(self.host))
                MESSAGE_ASK = "Connecting2SimpleImage"
                #self.tcpClientA.send(self.MESSAGE_ASK);
                self.tcpClient.send(MESSAGE_ASK)
                data = self.tcpClient.recv(self.BUFFER_SIZE)
            except Exception as e:
                print(e)
                print("host unreachable...will...try..to..connect again");
                continue;
        
            shaping = data.split(',')
            print shaping
        
            for i in range(0,len(shaping)):
                shaping[i] = int(shaping[i])
            self.BUFFER_SIZE = int(shaping[0])*int(shaping[1])*int(shaping[2])
            break;
            
    def getDataFromServer(self):
        self.data = ''
        self.tcpClient.send(self.MESSAGE)
        try:
            while len(self.data) < self.BUFFER_SIZE:
                self.data += self.tcpClient.recv(self.BUFFER_SIZE)
        except Exception:
                print("host unreachable")
                return None;
        return not None;
    def convertdata2depth(self):
        temp = np.frombuffer(self.data,dtype=np.uint8)
        h = np.asarray(temp[0::2],dtype=np.uint16)
        l = np.asarray(temp[1::2],dtype=np.uint16)
        res = (h << 8) + l
        print len(res)
        print self.shaping
        img = res.reshape(self.shaping[1],self.shaping[0])
        self.img = np.asarray(img >> 5,dtype=np.uint8)
        return not None
    def convertdata2image(self):
        try:
            self.img = np.frombuffer(self.data,dtype=np.uint8).reshape((int(self.shaping[0]),int(self.shaping[1]),int(self.shaping[2])))
        except Exception:
            return None;
        return not None;
