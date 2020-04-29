#Sean Nishi
#python version of my Always Watching security software

#TODO:
#1. need to put classifiers in a directory, scan for them, put them in list
#2. need to save video and after x-hours of recording, start new video, save old one, send old one to main computer
#3. need to take picture whenever a new person comes into view, send to main computer
#4. update database when we detect a new number of things we want to detect
#5. expand program to incoporate more than one camera, if >1 camera then create a thread for each extra camera
#6. need to add the commands for sending the pictures to google drive or something.

from threading import Thread
import cv2
import datetime
import time
import concurrent.futures

#face recognition libs
import pickle
import numpy as np

#flask stuff
from flask import Flask, Response, render_template
import imutils
import argparse

############################################################################################
#creates a thread to retrieve frames
class GetVideo:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.frame_width = int(self.stream.get(3))
        self.frame_height = int(self.stream.get(4))
        (self.grabbed, self.frame) = self.stream.read()
        self.thread = None
        self.stopped = False

    def start(self):
        self.thread = Thread(target = self.get, args = ()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True

############################################################################################
#creates a thread to display frames
class ShowVideo:
    def __init__(self, frame = None):
        self.frame = frame
        self.thread = None
        self.stopped = False

    def start(self):
        self.thread = Thread(target = self.show, args = ()).start()
        return self

    def show(self):
        while not self.stopped:
            cv2.imshow("Video", self.frame)
            if cv2.waitKey(1) == ord("q"):
                self.stop()

    def stop(self):
        self.stopped = True

#####################################################################
################################################################################
#function given to a thread
#Input: current frame we will look at, xml classifier path
#Output: returns a copy of the input frame with ellipses drawn on areas of interest, also updates database with new entry
def detect(Frame, path, last_num_detected, recognizer, label_dict):
    global num_pics
    global dbclient
    #global label_dict
    global last_num_profface_detected
    global last_num_frontface_detected

    frame = Frame
    num_things = 0
    classifier = cv2.CascadeClassifier(path)
    if not classifier:
        print("ERROR: bad path for classifier")
        exit(1)

    #gray out image before working on it
    grayCopy = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    detect = classifier.detectMultiScale(grayCopy, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    
    #for every detected face
    #see if we recognize them
    #draw an ellipse around every face
    for(x, y, w, h) in detect:
        roi_gray = grayCopy[y:y+h, x:x+w]

        #who is it? how confidant?
        id_, conf = recognizer.predict(roi_gray)
        if conf >=85:
            print("Hello " + label_dict[id_])
            cv2.putText(frame, label_dict[id_], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
        #circle roi where things are detected
        frame = cv2.ellipse(img=frame, center=(int(x+0.5*w), int(y+0.5*h)), axes=(int(w*0.5), int(h*0.75)), angle=0, startAngle=0, endAngle=360, color=(255, 0, 255), thickness=1)
        num_things+=1

        #if we arent sure who it is, take their picture
        if conf <90:
            if num_things > last_num_detected:
                #save frame
                path = str(new_person_pic_path + str(num_pics) + str(".png"))
                print("saving image at " + path)
                num_pics+=1
                cv2.imwrite(path, frame)
    
    last_num_detected = num_things
    return frame

###############################################################################
#creates threads for grabbing and showing video frames
#main thread passes the frames between them
def threads4All(args):
    src = 0
    last_num_profface_detected = 0
    last_num_frontface_detected = 0

    #init recognizer with frendly people (frontal face)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("face-trainer.yml")

    #load label dictionary for recognized people
    label_dict = {}
    with open("face-labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        #invert key, value pairs so it makes sense
        label_dict = {v:k for k,v in og_labels.items()}
    print(label_dict)
    
    #threads to get and display video
    getter = GetVideo(src).start()
    shower = ShowVideo(src).start()

    #output video
    recording = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 10, (getter.frame_width, getter.frame_height))

    while True:
        if getter.stopped or shower.stopped:
            getter.stop()
            shower.stop()
            break

        if getter.frame is not None:
            #make sure work is done on the same frame
            now = getter.frame

            #put time in bottom corner of screen
            timestamp = datetime.datetime.now()
            cv2.putText(now, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, now.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            
            #detect faces
            with concurrent.futures.ThreadPoolExecutor() as executor:
                face_future = executor.submit(detect, now, face_class_path, last_num_frontface_detected, recognizer, label_dict)
                #prof_future = executor.submit(detect, now, profface_class_path, last_num_profface_detected, recognizer, label_dict)

            #combine images to display one image
            #finalImage = cv2.add(face_future.result(), prof_future.result())

            finalImage = face_future.result()
            
            shower.frame = finalImage
            
            #give image to shower
            #shower.frame = finalImage

            #save frame to recording
            recording.write(finalImage)
            if cv2.waitKey(1) == ord("q"):
                break
            
    #cleanup
    recording.release()
    cv2.destroyAllWindows()
########################################################################
#set up
#paths to classifiers and init stuff
face_class_path = "cascades/haarcascade_frontalface_default.xml"
#profface_class_path = "cascades/haarcascade_profileface.xml"
new_person_pic_path = "pics/Detected_Face_"

args = None

num_pics = 0

print("Initiating the Always Watching Security System\n")
#start the program
threads4All(args)

