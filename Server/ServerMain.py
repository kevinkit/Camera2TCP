# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 07:57:07 2017

@author: khoefle
"""

import socket
import threading
import argparse
import sys
import numpy as np
import random
#import cv2
import time
import random
import sys
from sys import platform
import netifaces as ni
import zlib

def parse_args():
    """Parse input arguments
    """
    parser = argparse.ArgumentParser(description="Someday I will write something here.sry.")



    parser.add_argument('--Kinect',help='Disable/Enable Kinect, Default=True',default=True,type=bool)
    parser.add_argument('--Webcam',help='Disable/Enable Webcam, Default=True',default=True,type=bool)
    parser.add_argument('--Image',help='Used to send image for emulation',default='lena.png')
    parser.add_argument('--Port',help='Port number for communcation',default=8080,type=int)
    parser.add_argument('--Change',help='Allow changing the image for debugging',default=True)
    parser.add_argument('--Debug',help='Allow Debuging (sending one image)',default=True)
    args = parser.parse_args()
    return args





if __name__ == "__main__":

   # Kinect = False;
    if platform == "win32":
        ip = socket.gethostbyname(socket.gethostname());
    else:
        try:
            ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']    
        except:
            ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']   
    args = parse_args()
    if not Kinect:
        args.Kinect =  Kinect;
        print("NO KINECT FRAMEWORK INSTALLED!")
    print("I am on: " + ip)
    TS = ThreadedServer(ip,args.Port,image_name=args.Image,change=args.Change,Debug=args.Debug)

    t = threading.Thread(target=TS.listen)
    t.start();

    while(1):
        try:
            print("I am on: " + ip)
            print (TS.cnt)
            if args.Kinect:
                print("Kinect available")
            if TS.ret:
                print(TS.RGB0.shape)
                print(TS.RGB0.size)
                print(type(TS.RGB0))
                print(TS.log)

                cv2.imshow('Server: ' + ip + ":" + str(args.Port),TS.RGB0)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print("no cam detected!")
                print(TS.log)

                cv2.imshow('Server: ' + ip + ":" + str(args.Port),TS.img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                if TS.ImageT.isAlive():
                    print("image thread alive")
                else:
                    print("image thread dead")
        except KeyboardInterrupt:
            break;

    #Clean up
    TS.sock.close();
    TS.alive = False;


    if args.Kinect:
        TS._kinect.close()

    TS._done = True;
    if t.isAlive():
        print("closing...")
        t.join(0.1);
        print("closed...")
