
# Camera2TCP



This repository is a python framework for making camera data available via TCP.
Currently it only runs on Python 2.7, due to some old print statements. 

# Getting started


This chapter will give a quick overview on how to start the project. For details see later chapters in this Readme.

The Threaded server is the one providing the images, either from a camera, a kinect or from a webcam. The client is the one asking for those pictures. The client needs to know the IP-Adress of the Server.

1. Start the Server. Here for example with a webcam. 
```
python ThreadedServer.py --Webcam 
```
2. On the same, or on any other machine start the Client and specify the wanted Service from the Server (Here a Webcam, like started on the Server). Here, the Server has the IP 192.178.2.10 and the wanted 
```
python Client.py --HOST 192.168.2.10 --Service RGBWebcam
```

# IMPORTANT

## Dependencies:


### Must-Have:

* socket
* netifaces
* threading
* sys
* numpy
* Either opencv (python) 
* time
* ctypes
* pygame


* pykinect2 and so the Windows SDK for Kinect

## Server

Server was only tested on Windows.


## Clients

Clients run on Windows and Linux. 


## Known bugs and fixes:

* Do not call the ThreadedServer script in Spyder. Use python shell.
* Do not call any Client script in Spyder. Use python shell
* The ThreadedServer does not stop properly. To stop it close the popped up window (yes it will crash...)
* Close clients with str+c in the command line

* AssertionError -80: This is a bug coming from the pykinect framework. To resolve this simply replace the files installed from pip by the ones from the offical repository, which can be found here: https://github.com/Kinect/PyKinect2


## Upcoming features:

* Bug fixes
* Sending multiple images from directory
* Sending video


# Version 0.2 is on #

The first connections are done.
Several bugs fixed
Single image can be send
Arguments can now be parsed

# Overview Clients

All clients ending with a letter like A,B,C... are depricated. Use the Client.py instead.

## Arguments:

### Service

Determines the Service one whiches to connect to. Currently there are the following options available:

* SimpleImage (Just one image that gets alternated)
* RGBWebcam (Conneting to a simple WebCam)
* KinectWebcam (Connecting to Kinect RGB)
* KinectSkeleton (Not working)
* KinectDepth (Connecting to Kinect Depth Sensors)

### HOST

Sets the IP-Adress, default will be the local machine IP-Adress.

### PORT 

Sets the PORT to connect to, default is 8080.

### Show

Enables or disables showing the image after recieving it. Default is enabled.
### Write

Enables or disables writing the recieved image to file. Note: The file will be overwritten at any frame. Default is disabled. 

# Overview ThreadedServer

The ThreadedServer is a threaded TCP Server, which is capable of distributing the data to several clients.

## Arguments:

### Kinect 

Disables / Enables the Kinect. Default = Enabled
If the Kinect Framework fails to load, the Kinect services are disabled.

### Webcam

Disables / Enables the Webcam. Default = Enabled

### Image

Gives the path to the image which will be send

### Port

Sets the port the Server runs on.

### Change

Allows to alter the image loaded from the Image parameter. It will make additions to the pixel so one is able to see wether several frames or just one frame is recieved by the client.

### Debug

Allow Debuging, which is mainly the sending of the one image loaded by the Image paramter and alternated from the change parameter. 


# LEGAL DISCLAIMER


The image lena.png is owned by "Playmate of the Month". Playboy Magazine. November 1972, photographed by Dwight Hooker


