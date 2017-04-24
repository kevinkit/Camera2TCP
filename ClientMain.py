# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 21:54:51 2017

@author: Kevin
"""

import cv2
import Client
import argparse
import socket

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
    client = Client.Client(ConnectionType=args.Service,show=args.Show,write=args.Write,IP=args.HOST,Port=args.PORT)
    ret = client.initConnection()

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
                    cv2.imwrite('something.png',client.img);
                except Exception as e:
                    print(e)
