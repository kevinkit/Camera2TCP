# Camera2TCP
This repository is a python framework for making camera data available via TCP


# IMPORTANT

## Dependencies:


### Must-Have:

* socket
* threading
* sys
* numpy
* opencv (python)
* pykinect2 
* ctypes
* pygame


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
* Parsing of Input Parameters instead of having to change code


# Version 0.1 is on #

The first connections are done.

# Overview Clients

## IP-Adress

All clients have a variable called "host". Currently this host gets set by 

```
 host = socket.gethostbyname(socket.gethostname())
```
Which will set the client-socket directly on the host machine. This means that this is not a direct connetoion on the network, but on the machine itself. To have a connetion to an other machine simply change the line to the desired IP-Adress as a string, like:

```
 host = '192.168.2.10'
```

## Port

The current used Port on any client is 2004. To change it, simply change the variable in the script. 

## Client A

Client A is for a simple webcam,it connects to the server with the message "Connecting2RGBWebcam" , which answer with the resolution, which can be of any kind. After this the client proceeds to send the Message "RGB" to the server which answers with an obtained color frame

## Client B

Client B is for a connection to a Kinect v2. The Client connects with the message "Connecting2KinectWebcam", the Server answers with the static information of the HD-Resolution. Further releases should take in consideration that this may be adapted. After this the client proceeds to send "RGBHD" , the server answers with a new RGBA-frame obtained by the Kinect v2 if there is a new one available.


## Client C

Client C should be for Skeleton data, but it does not work atm.

## Client D

Client B is for a connection to a Kinect v2. The Client connects wit the message "Connecting2KinectDepth" and recieves the static information of the Depth-Frame resolution. Further releases should take in consideration that this may be adapted. After this the client proceeds to send "Depth"



# Overview ThreadedServer

The ThreadedServer is a threaded TCP Server, which is capable of distributing the data to several clients.

## IP-Adress

The Server automatically uses the IP-Adress obtained by the line


```
 TS = ThreadedServer(socket.gethostbyname(socket.gethostname()),port_num)
```

To run it on a specific IP change the line to for example:

```
 TS = ThreadedServer('192.168.2.10',port_num)
```

## Port 

The Port is currently set by the variable 

```
 port_num = 2004
```
To use an other port simply change the variable.




