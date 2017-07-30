# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 18:59:08 2017

@author: kevinkit


Please see:

http://stackoverflow.com/questions/23828264/how-to-make-a-simple-multithreaded-socket-server-in-python-that-remembers-client
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
missings = 0



Kinect = True;
Camera = True;

try:
    import cv2
except ImportError:
    print("Missing OpenCV!")
    Camera = False;
#Advanced in case that Kinect is installed
try:
    from pykinect2 import PyKinectV2
    from pykinect2.PyKinectV2 import *
    from pykinect2 import PyKinectRuntime
    import ctypes
    import _ctypes
    import pygame
    import sys
except ImportError:
    print("Missing libs for Kinet!")

    if not Camera:
        print("No library for camera detection found, neither OpenCV nor Kinect")
        sys.exit()
    else:
        Kinect = False;

#Check every 10 Seconds if the thread should be dead
socket.setdefaulttimeout(10)
# colors for drawing different bodies

if Kinect:
    SKELETON_COLORS = [pygame.color.THECOLORS["red"],
                      pygame.color.THECOLORS["blue"],
                      pygame.color.THECOLORS["green"],
                      pygame.color.THECOLORS["orange"],
                      pygame.color.THECOLORS["purple"],
                      pygame.color.THECOLORS["yellow"],
                      pygame.color.THECOLORS["violet"]]

def RandThread(retval,i):
    retval[i] = random.randint(0,255)

retval = [None];
T = threading.Thread(target=RandThread,args=[retval,0])
T.start()


class ThreadedServer(object):


    def __init__(self, host, port,camtype="webcam",ID=0,image_name='lena.png',change=True,Debug=True):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.comThreads = []
        self.alive = True;
        self.RGB0 = [];
        self.Depth = [];
        self.Body = [];
        self.camtype = camtype;
        self.ret = False;
        self.log = "test"
        self.HDRGB = [];
        self.imageName = image_name;
        self.change = change;
        self.sys_random = random.SystemRandom();
        #Assuming 8bit pic
        self.cnt = 0;
        self.trip = 0;
        self.Debug = Debug

        self.send_counter = 0;
        self.rgb_cnt = 0;
        #Locks
        self.Lock  = threading.Lock()

        if self.Debug:
            self.img = cv2.imread(self.imageName); #This one will be altered!
            self.orig_img = cv2.imread(self.imageName); #This one will be the same
            self.ImageT = threading.Thread(target=self.imagechanger)
            self.ImageT.start()
            self.height,self.width,self.channel = self.img.shape;
            self.x_pos = random.randint(10,self.width);
            self.y_pos = random.randint(10,self.height);
            if self.ImageT.isAlive():
                self.log = "height: " + str(self.height)
        if Kinect:
            pygame.init()


            #Used to manage how fast the screen updates
            self._clock = pygame.time.Clock()
            self._done = False;
            self._infoObject = pygame.display.Info()
            self._screen = pygame.display.set_mode((self._infoObject.current_w >> 1, self._infoObject.current_h >> 1),
                                       pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)



            # Kinect runtime object, we want only color and body frames
            self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body | PyKinectV2.FrameSourceTypes_Depth | PyKinectV2.FrameSourceTypes_Infrared)
            # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
            self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)
            # here we will store skeleton data
            self._bodies = None

        if camtype == "webcam":

            self.cap = cv2.VideoCapture(ID)


    def imagechanger(self):
        while self.alive:
        #    self.lock.acquire(True)
            #self.img = self.img + 10
            
            self.send_counter = self.send_counter + 1;
            
            #self.rgb_cnt
            
            
    
            

            if self.send_counter % 255  == 0:
                if self.rgb_cnt != 2:
                    self.rgb_cnt = self.rgb_cnt + 1;
                else:
                    self.rgb_cnt = 0;
                    #Get the new random positions
                    self.x_pos = random.randint(10,self.width);
                    self.y_pos = random.randint(10,self.height)

            
                self.send_counter = 0;
     

            #if self.send_counter % 99999 == 0:
            time.sleep(0.03)
            #sendstr = str(self.send_counter) 
            if self.rgb_cnt == 0:
                
               cv2.putText(self.img,"hello from", (self.x_pos+self.send_counter,self.y_pos), cv2.FONT_HERSHEY_SIMPLEX, 2, [0,0,self.send_counter])
               cv2.putText(self.img,"the Server", (self.x_pos + 100+self.send_counter,self.y_pos +100), cv2.FONT_HERSHEY_SIMPLEX, 2, [0,0,self.send_counter])
            elif self.rgb_cnt == 1:
               cv2.putText(self.img,"hello from", (self.x_pos+self.send_counter,self.y_pos+self.send_counter), cv2.FONT_HERSHEY_SIMPLEX, 2, [0,self.send_counter,255])
               cv2.putText(self.img,"the Server", (self.x_pos +100 +self.send_counter,self.y_pos +100), cv2.FONT_HERSHEY_SIMPLEX, 2, [0,self.send_counter,255])
            elif self.rgb_cnt == 2:
               cv2.putText(self.img,"hello from", (self.x_pos+self.send_counter,self.y_pos-self.send_counter), cv2.FONT_HERSHEY_SIMPLEX, 2, [255,255,self.send_counter])
               cv2.putText(self.img,"the Server", (self.x_pos + 100+self.send_counter,self.y_pos + 100), cv2.FONT_HERSHEY_SIMPLEX, 2, [255,255,self.send_counter])
            self.log = str(self.send_counter)
        #    self.lock.release()
        #time.sleep(1)

    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        print(frame.size)
        del address
        target_surface.unlock()

    def getLena(self):
        img = cv2.imread('lena.png')
        return img;


    def listenWrapper(self,client,address):
        client, address = self.sock.accept()

    def getRGB(self):
        if self.camtype == "webcam":
            ret, frame = self.cap.read()
            self.ret = ret;
            if ret:
                 self.RGB0 = frame;
                 return ret,frame
            else:
                 return ret, None
    def listen(self):
        self.sock.listen(5)
        while True:
            try:
                client, address = self.sock.accept()
                client.settimeout(60)
                threading.Thread(target = self.listenToClient,args = (client,address)).start()
            except socket.timeout:
                if self.alive:
                    continue;
                else:
                    break;
    def getHDRGB(self):
            self.log = "Captured events"
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                self.draw_color_frame(frame, self._frame_surface)
                self.HDRGB = frame;#frame.tolist()

                # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
                # --- (screen size may be different from Kinect's color frame size)
                h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
                target_height = int(h_to_w * self._screen.get_width())
                surface_to_draw = pygame.transform.scale(self._frame_surface, (self._screen.get_width(), target_height));
                self._screen.blit(surface_to_draw, (0,0))
                surface_to_draw = None
                pygame.display.update()

                # --- Go ahead and update the screen with what we've drawn.
                pygame.display.flip()

                return frame;
            else:
                return None;

    def getSkeleton(self):
        if self._kinect.has_new_body_frame():
            self._bodies = self._kinect.get_last_body_frame()
            print self._bodies.bodies.all()

        if self._bodies is not None:
            return self._bodies;
        else:
            return None;

    def draw_body_bone(self, joints, jointPoints, color, joint0, joint1,client):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked):
            return None, None

        # both joints are not *really* tracked
        if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
            return None, None

        # ok, at least one is good
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)

        try:
            pygame.draw.line(self._frame_surface, color, start, end, 8)
    #        client.send("test")
    #        client.send(np.asarray(start,end))
            return start,end;
        except: # need to catch it due to possible invalid positions (with inf)
            return None, None
            pass

    def draw_body(self, joints, jointPoints, color,client):
        # Torso
        start = []
        end = []
        client.send("test3")
        s,e = self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck,client);
        start.append(s)
        end.append(e)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder,client);
        start.append(s)
        end.append(e)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid,client);
        start.append(s)
        end.append(e)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase,client);
        start.append(s)
        end.append(e)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderRight,client);
        start.append(s)
        end.append(e)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderLeft,client);
        start.append(s)
        end.append(e)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight,client);
        start.append(s)
        end.append(e)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft,client);
        start.append(s)
        end.append(e)
        # Right Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight,client);
        start.append(s)
        end.append(e)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight,client);
        start.append(s)
        end.append(e)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight,client);
        start.append(s)
        end.append(e)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandRight, PyKinectV2.JointType_HandTipRight,client);
        start.append(s)
        end.append(e)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_ThumbRight,client);
        start.append(s)
        end.append(e)
        # Left Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft,client);
        start.append(s)
        end.append(e)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft,client);
        start.append(s)
        end.append(e)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft,client);
        start.append(s)
        end.append(e)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandLeft, PyKinectV2.JointType_HandTipLeft,client);
        start.append(s)
        end.append(e)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft,client);
        start.append(s)
        end.append(e)
        # Right Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight);
        start.append(s)
        end.append(e)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_AnkleRight);
        start.append(s)
        end.append(e)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_FootRight);
        start.append(s)
        end.append(e)
        # Left Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft);
        start.append(s)
        end.append(e)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft);
        start.append(s)
        end.append(e)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft);
        start.append(s)
        end.append(e)

        return start,end

    def listenToClient(self, client, address):
        size = 1024
        while self.alive:
            try:
                data = client.recv(size)
                self.log = data;
                if data:
                    #Send specific frame stuff
                    if data == "Connecting2RGBWebcam":
                        self.log = "capturing"
                        re,frame = self.getRGB()
                        if re:
                             self.log = "succesful init capture"
                             client.send(str(int(self.RGB0.shape[0])) + ',' + str(int(self.RGB0.shape[1]))+ ',' + str(int(self.RGB0.shape[2])))
                        else:
                             print("no service available")
                             self.log = "unsuccesful capture"
                             client.send("no service available")
                    elif data == "RGBWebcam":
                        re,frame = self.getRGB()
                        if re:
                            client.send(self.RGB0)
                            self.log  = "succesful loop capture"
                        else:
                            self.log = "unsuccesful loop capture"
                        #self.ret = False;
                    elif data == "Connecting2KinectWebcam":
                            client.send("1080," + "1920," + "3")
                    elif data == "Connecting2KinectSkeleton":
                            client.send(str(self._kinect.max_body_count))
                    elif data == "Connecting2KinectDepth":
                            client.send("512," + "424," + "1")
                    elif data == "KinectWebcam":
                            self.log = "start computation"
                            frame = self.getHDRGB()
                            if frame is not None:
                                frame = np.delete(frame,np.arange(3,frame.size,4))
                                client.send(np.asarray(frame))
                                self.log = "send frame"
                            else:
                                client.send("no frame")
                                self.log = "no frame"
                    elif data == "KinectSkeleton":
                        self.log = "bodies: "  + str(self._bodies)
                        #client.send(np.asarray(self._bodies));
                        data = []
                        if self._kinect.has_new_body_frame():
                            self._bodies = self._kinect.get_last_body_frame()
#                            client.send("new body frame")
                            miss_cnt = 0
                            for i in range(0,self._kinect.max_body_count):
                                body = self._bodies.bodies[i]
                                if not body.is_tracked:
                                    miss_cnt = miss_cnt + 1;
                                    continue
                                joint_points = self._kinect.body_joints_to_color_space(joints)
                                for j in range(0,5):
                                    data.append(joint_points[i])


                            if miss_cnt == self._kinect.max_body_count:
                                client.send("no tracked bodies")
                            else:
                                client.send("on track")
                                #client.send(np.asarray(data))
                        else:
                            client.send("no bodies")
                    elif data == "KinectDepth":
                        if self._kinect.has_new_depth_frame():
                            depthframe = self._kinect.get_last_depth_frame();
                            self.log = len(depthframe)
                            low = np.asarray(depthframe,dtype=np.uint8);
                            high = np.asarray((depthframe >> 8),dtype=np.uint8)
                            #f = np.c_[high,low].ravel()
                            f = np.vstack((high, low)).ravel('F')
                            self.log = len(f)
                            #self.log = np.asarray(depthframe,dtype=np.uint8)
                            client.send(np.asarray(f))
                        else:
                            client.send("no depth frame")
                    elif data == 'Connecting2SimpleImage':
                            self.log = self.Debug
                            if self.Debug:
                                client.send(str(int(self.img.shape[0])) + ',' + str(int(self.img.shape[1]))+ ',' + str(int(self.img.shape[2])))
                            else:
                                client.send("Invalid Request")

                    elif data == "SimpleImage":
                            if self.Debug:
                                self.log = "sending"
                                client.send(self.img)
                                self.img = self.orig_img;
                            else:
                                client.send("Invalid Request")
                    else:
                        client.send("Invalid request")



                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

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


    args = parse_args()
    if not Kinect:
        args.Kinect =  Kinect;
        print("NO KINECT FRAMEWORK INSTALLED!")
    print("I am on: " + socket.gethostbyname(socket.gethostname()))
    TS = ThreadedServer(socket.gethostbyname(socket.gethostname()),args.Port,image_name=args.Image,change=args.Change,Debug=args.Debug)

    t = threading.Thread(target=TS.listen)
    t.start();

    while(1):
        try:
            print("I am on: " + socket.gethostbyname(socket.gethostname()))
            print TS.cnt
            if args.Kinect:
                print("Kinect available")
            if TS.ret:
                print(TS.RGB0.shape)
                print(TS.RGB0.size)
                print(type(TS.RGB0))
                print TS.log

                cv2.imshow('Server: ' + socket.gethostbyname(socket.gethostname()) + ":" + str(args.Port),TS.RGB0)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print("no cam detected!")
                print TS.log

                cv2.imshow('Server: ' + socket.gethostbyname(socket.gethostname()) + ":" + str(args.Port),TS.img)
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
