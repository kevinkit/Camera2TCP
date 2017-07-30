# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 21:54:51 2017

@author: Kevin
"""

import cv2
import Client
import argparse
import socket
import time as ti
import threading
import os
import sys
from sys import platform
import netifaces as ni
def parse_args():
    """Parse input arguments
    """
    parser = argparse.ArgumentParser(description="Someday I will write something here.sry.")
    parser.add_argument('--Service',help='Kind of Service', default=['SimpleImage'],
                        choices=['SimpleImage','RGBWebcam','KinectWebcam','KinectSkeleton','KinectDepth'])
    
    if platform == "win32":
        parser.add_argument('--HOST',help='Define IP adres',nargs='+',default=[socket.gethostbyname(socket.gethostname())])
    else:
        try:
            ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']    
        except:
            ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']     
        parser.add_argument('--HOST',help='Define IP adres',nargs='+',default=[ip])
    parser.add_argument('--PORT',help='Define PORT used',nargs='+',default=[8080],type=int)
    parser.add_argument('--Show',help='Disable/Enable showing,default=True',default=True)
    parser.add_argument('--Write',help='Dsiable/Enable writing image files',default=[False])
    parser.add_argument('--camId',help='set the id of the camera',default=[0],type=int)

    args = parser.parse_args()
    return args


class ClientWrapper():
    def __init__(self,client):
        self.client = client;
        self.ret = [None]*len(client)
        #Start a thread for every client
        for i in range(0,len(self.client)):
            threading.Thread(target = self.communcation,args=[i]).start()
            

    def communcation(self,i):
        imgNr = 0;
        self.ret[i] = self.client[i].initConnection()
        #if self.ret[i] is not None:
        while self.ret[i] is not None:
            self.ret[i] = self.client[i].getDataFromServer()
            if self.ret[i] is not None:
                if client[i].connectionType != 'KinectDepth':
                    self.ret[i] = self.client[i].convertdata2image()
                else:
                    self.ret[i] = self.client[i].convertdata2depth()    
            if self.ret[i] is not None:
                if self.client[i].show:
                    try:
                        cv2.imshow(self.client[i].connectionType + 'from: ' + str(self.client[i].host) + ":" + str(self.client[i].port) ,self.client[i].img)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    except Exception as e:
                        print(e)
                if self.client[i].write:
                    try:
                        cv2.imwrite('cam' + str(self.client[i].camId) + '/' + str(ti.time()) + '_Cam' + str(self.client[i].camId) + '_Image' + str(imgNr) +'.png', self.client[i].img);
                        imgNr = imgNr + 1
                    except Exception as e:
                        print(e)
if __name__ == "__main__":

   # Kinect = False;
    args = parse_args()
    
    if len(args.HOST) != len(args.PORT):
        print("Host List does not match Port list, taken first Port for all Hosts")
        Port = [args.PORT[0]] * len(args.HOST);
    else:
        Port = args.PORT;
    
    if len(args.HOST) != len(args.Service):
        print("Host List does not match Service list, taken first Service for all Hosts")
        Service = [args.Service[0]] * len(args.HOST);
    else:
        Service = args.Service;
    
    if len(args.HOST) != len(args.Write):
        print("Host List does not match Write enabling list, taken first Disable/Enable for all Hosts")
        Write = [args.Write[0]] * len(args.HOST);
    else:
        Write = args.Write;
    
    
    
    if len(args.HOST) != len(args.camId):
        print("Camera index does not match Host lsit, therefore using the first one as start point")
        camId = range(args.camId[0],len(args.HOST));
    else:
        camId = args.camId;
    
    
    
    
    print Service
    print Port
    print args.HOST
    print Write
    print camId
    cnt = 0;
    client = [None]*len(args.HOST)
    print client
    for host in args.HOST:
        print cnt
            
        print Service[cnt]
        print Write[cnt]
        print host
        print Port[cnt]
        client[cnt] = Client.Client(ConnectionType=Service[cnt],show=args.Show,write=Write[cnt],IP=host,Port=Port[cnt],camId=camId[cnt])
        if client[cnt].write:
            imgNr = 0
            if( not os.path.isdir('./cam' + str(client[cnt].camId))):
                os.mkdir('./cam' + str(client[cnt].camId))
        cnt = cnt + 1;
    #Start the class
    ClientWrapper(client);


#        ret[cnt] = client[cnt].initConnection()
#      
#   
#        if client[cnt].write:
#            imgNr = 0
#            if( not os.path.isdir('./cam' + str(client[cnt].camId))):
#                os.mkdir('./cam' + str(client[cnt].camId))
#        cnt = cnt + 1;
#        
#        if ret[cnt] is not None:
#            
#    
#    
#    while ret is not None:
#        ret = client.getDataFromServer()
#        if ret is not None:
#            if client.connectionType != 'KinectDepth':
#                ret = client.convertdata2image()
#            else:
#                ret = client.convertdata2depth()                                                                                        
#        if ret is not None:
#            if client.show:
#                try:
#                    cv2.imshow(args.Service + 'from: ' + args.HOST + ":" + str(args.PORT) ,client.img)
#                    if cv2.waitKey(1) & 0xFF == ord('q'):
#                        break
#                except Exception as e:
#                    print(e)
#            if client.write:
#                try:
#                    cv2.imwrite('cam' + str(client.camId) + '/' + str(ti.time()) + '_Cam' + str(client.camId) + '_Image' + str(imgNr) +'.png', client.img);
#                    imgNr = imgNr + 1
#                except Exception as e:
#                    print(e)
