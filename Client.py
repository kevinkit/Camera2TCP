# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 12:10:39 2017

@author: Kevin
"""

#General classs for Connecting to any kind of Service



import argparse
import socket
import numpy as np
import cv2

class Client(object):
    def __init__(self,ConnectionType='SimpleImage',show=False,write=False,IP=socket.gethostbyname(socket.gethostname()),Port=8080):
        self.connectionType = ConnectionType;
        self.host = IP
        self.show = show;
        self.write = write;
        self.port = Port;
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
                    self.BUFFER_SIZE = int(self.shaping[0])*int(self.shaping[1])*int(self.shaping[2])
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
    def convertdata2image(self):
        try:
            self.img = np.frombuffer(self.data,dtype=np.uint8).reshape((int(self.shaping[0]),int(self.shaping[1]),int(self.shaping[2])))
        except Exception:
            return None;
        return not None;
     
def parse_args():
    """Parse input arguments
    """
    parser = argparse.ArgumentParser(description="Someday I will write something here.sry.")
    parser.add_argument('--Service',help='Kind of Service', default='SimpleImage',
                        choices=['SimpleImage','RGBWebcam','KinectWebcam','KinectSkeleton','KinectDepth'])
    parser.add_argument('--HOST',help='Define IP adres',default=socket.gethostbyname(socket.gethostname()))
    parser.add_argument('--PORT',help='Define PORT used',default=8080,type=int)
    parser.add_argument('--Show',help='Disable/Enable showing,default=True',default=True)
    parser.add_argument('--Write',help='Dsiable/Enable writing image files',default=False)

    args = parser.parse_args()
    return args





if __name__ == "__main__":

   # Kinect = False;
    args = parse_args()
    client = Client(ConnectionType=args.Service,show=args.Show,write=args.Write,IP=args.HOST,Port=args.PORT)
    ret = client.initConnection()

    while ret is not None:
        ret = client.getDataFromServer()
        if ret is not None:
            ret = client.convertdata2image();
        if ret is not None:
            if client.show:
                try:
                    cv2.imshow('something',client.img)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                except Exception as e:
                    print(e)
            if client.write:
                try:
                    cv2.imwrite('something.png',client.img);
                except Exception as e:
                    print(e)
    
    
    
    
