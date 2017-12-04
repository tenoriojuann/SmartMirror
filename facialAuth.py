import face_recognition
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import os
import webbrowser
import sys
import picamera
import imutils
import tkinter as tk
import time

import numpy as np

from db import DB

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)

# provide name of image
process_this_frame = True
detect_motion = True
is_user_viewing = False

def monitor():
    movement_counter = 0
    should_break = False
    camera = picamera.PiCamera()
    camera.vflip = True
    rawCapture = PiRGBArray(camera)
    camera.resolution = (320, 240)
    camera.framerate = 30
    time.sleep(2)
    firstFrame = None
    detect_motion = True;
    #cam = cv2.VideoCapture(0)
    while detect_motion:
        for test in camera.capture_continuous(rawCapture, format="bgr"):
            #frame = cam.read()[1]
            #if should_break:
            #    break
            #frame = imutils.resize(frame, width=500)
            testImage = rawCapture.array
            # test_image = rawCapture.array
            cv2.imwrite("test.jpg", testImage)
            #coversts to grey
            frame = testImage

            currentFrame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            #Performs Gaussian Blure on image
            currentFrame = cv2.GaussianBlur(currentFrame, (15,15), 10)
            cv2.imwrite("grey_blur.jpg", currentFrame)
            # If we have not established a first frame( the basis of all of our motion tracking) then we establish it here
            if firstFrame is None:
                print("Got first frame")
                # Save first frame
                firstFrame = currentFrame
                cv2.imwrite("first.jpg", firstFrame)
                #Starts over
                rawCapture.truncate(0)
                # Starts over
                continue
            # Calculates Agsolute Difference between the first frame and the current frame
            frameDelta = cv2.absdiff(firstFrame, currentFrame)
            #Writes out frameDelta as jpg
            cv2.imwrite("frameDelta.jpg", frameDelta)
            #Does the threshold of the image(may need tweeking depending on environment)
            thresh = cv2.threshold(frameDelta, 30, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            # Writes out thresh image as thresh.jog
            cv2.imwrite("thresh.jpg", thresh)
            # Finds contours within the thresh image
            (cnts, contours, _) = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            print("got contours")
            for count in contours:
                print("Getting areas")
                area = cv2.contourArea(count)
                print(area)
                # If size of contour is not big enough, ignore it(aka, if the movement is not big enough ignore it)
                if cv2.contourArea(count) < 500:
                    continue
                # We look for three points of movement within any check
                else:
                    movement_counter += 1
                    print("Movement, Movement#: " + str(movement_counter)+ "Area: " + str(area))
                    # If mwe detect 3 points of movement we begin facial authentication
                    if movement_counter == 1:
                        #Frame represnets the current frame of the system.
                        #TODO redo facial_
                        face_recognition = Facial(os.path.dirname(__file__))
                        try:
                            authentication_results = face_recognition.facial_authenticate(frame)
                        except:
                            authentication_results = "Exception"
                        print ("Try To Authenticate")
                        print(authentication_results)
                        rawCapture.truncate(0)
                        should_break = True
                        break;
            rawCapture.truncate(0)
            break;
        rawCapture.truncate(0)
        continue




class Facial:

    def __init__(self, root):
        self.database = DB(root)



    def facial_authenticate(self,image):
        global detect_motion
        cv2.imwrite("test2.jpg", image)
        # Resize frame of video to 1/4 size for faster face recognition processing
        #small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
        try:
            print("about to get DB")
            user_face_dict = self.get_all_email_images()
            print("about to proces emails")
            for key in user_face_dict.keys():
                print(key)
                script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
                rel_path = "Images/" + key + ".jpg"
                print("fA:"+rel_path)
                abs_file_path = os.path.join(script_dir, rel_path)
                print("fA:"+abs_file_path)
                user_image = face_recognition.load_image_file(abs_file_path)
                print("doing face encoding for db image")
                user_face_encoding = face_recognition.face_encodings(user_image)[0]
                #print("looking for face locations in image passed in")
                #face_locations = face_recognition.face_locations(image)
                #print("doing face encoding for image passed in")
                print("loading test file")
                test_image = face_recognition.load_image_file("test2.jpg")
                print("getting test image encoding")
                face_encodings = face_recognition.face_encodings(test_image)[0]
                print("about to do face comparissons")
                tot = 0
                for face_encoding in face_encodings:
                    print("in loop")
                    match = face_recognition.compare_faces([user_face_encoding], face_encoding)
                    tot += 1
                    print(tot)
                    status = "Unknown"

                    if match:
                        status = "Success"
                        print(status + " : "+ key)
                        webbrowser.open_new_tab("http://172.20.10.8:5000/mirror/"+key)
                        detect_motion = False
                        is_user_viewing = True
                        print("sleeping for 30 seconds")
                        time.sleep(30)
                        print("Monitoring")
                        return True
                    else:
                        print(status)
                        break;

                    face_names.append(status)
        except:
            e = sys.exc_info()[0]
            print("<p>Error: %s</p>" % e)

    def captureImage(self,userName):
        global process_this_frame
        camera = picamera.PiCamera()
        rawCapture = PiRGBArray(camera)
        camera.resolution = (500, 420)
        camera.framerate = 30
        camera.vflip = True
        time.sleep(2)
        ret_img = None;
        process_this_frame = False
        for image in camera.capture_continuous(rawCapture, format="bgr"):
            print("Image Captured")
            img = rawCapture.array
            script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
            rel_path = "Images/"+userName+".jpg"
            abs_file_path = os.path.join(script_dir, rel_path)
            print(abs_file_path)
            cv2.imwrite(abs_file_path, img)
            ret_img = img
            rawCapture.truncate(0)
            camera.close()
            return ret_img

    def get_all_email_images(self):
        try:
            emails = self.database.getEmail()
            user_image_dict = {}
            for email in emails:
                a_user_image = face_recognition.load_image_file("Images/" + email[0] + ".jpg")
                user_image_dict[email[0]] = a_user_image
            return user_image_dict
        except:
            e = sys.exc_info()[0]
            print("<p>Error: %s</p>" % e)