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
import os

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
    parser.add_argument('--camId',help='set the id of the camera',default=0,type=int)

    args = parser.parse_args()
    return args



if __name__ == "__main__":

   # Kinect = False;
    args = parse_args()
    client = Client.Client(ConnectionType=args.Service,show=args.Show,write=args.Write,IP=args.HOST,Port=args.PORT,camId=args.camId)
    ret = client.initConnection()
    
    if client.write:
        imgNr = 0
        if( not os.path.isdir('./cam' + str(client.camId))):
            os.mkdir('./cam' + str(client.camId))

    while ret is not None:
        ret = client.getDataFromServer()
        if ret is not None:
            if client.connectionType != 'KinectDepth':
                ret = client.convertdata2image()
            else:
                ret = client.convertdata2depth()                                                                                        
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
                    cv2.imwrite('cam' + str(client.camId) + '/' + str(ti.time()) + '_Cam' + str(client.camId) + '_Image' + str(imgNr) +'.png', client.img);
                    imgNr = imgNr + 1
                except Exception as e:
                    print(e)
