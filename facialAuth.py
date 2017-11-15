import face_recognition
import cv2
import os
import webbrowser
import sys
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

#provide name of image
database = DB("/Users/jsexton/Senior")
process_this_frame= True

def get_all_email_images():
    emails = database.getEmail()
    user_image_dict = {}
    for email in emails:
        a_user_image = face_recognition.load_image_file(email[0] + "/" + email[0] + ".jpg")
        user_image_dict[email[0]] = a_user_image
    return user_image_dict

def diffImg(i1, i2, i3):
    d1 = cv2.absdiff(i1,i2)
    d2 = cv2.absdiff(i1,i3)
    ret, thres = cv2.threshold(i1, 10, 0xff, cv2.THRESH_BINARY)
    #print (d1)
    #print (d2)
    if ((d1 != d2).all()):
        print("Movement!")
    else:
        print("No Movement!")
    return cv2.bitwise_and(d1,d2)

def monitor():
    movement_counter = 0
    cam = cv2.VideoCapture(0)
    test = cam.read()[1]
    firstFrame = None
    while True:
        frame = cam.read()[1]
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (15,15), 0)
        cv2.imwrite("grey_blur.jpg", gray)
        if firstFrame is None:
            print("Got first frame")
            firstFrame = gray
            cv2.imwrite("first.jpg", firstFrame)
            continue
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cv2.imwrite("thresh.jpg", thresh)
        (cnts, contours, _) = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            area = cv2.contourArea(c)
            #print(area)
            if cv2.contourArea(c) < 1000:
                continue
            else:
                movement_counter+=1
                print("Movement")
                if movement_counter % 3 == 0:
                    ret, image = cam.read()
                    if ret:
                        cv2.imwrite("test1.jpg", image)
                        fac = facial_authenticate(image)
                        print (fac)
                        if fac is True:
                            print("Success!")
                        else:
                            continue

   ## while True:
   ##     cv2.imshow(window, diffImg(image_minus, image_base, image_plus))
   ##     image_minus = image_base
   ##     image_base = image_plus
   ##     image_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

   ##     key = cv2.waitKey(10)
   ##     if key == 27:
   ##         print("Goodbye")
   ##         break

def facial_authenticate(image):
    process_this_frame = True
    while process_this_frame:
        # Grab a single frame of video
        cv2.imwrite("test2.jpg", image)
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
        try:
            if process_this_frame:
                user_face_dict = get_all_email_images()
                for key in user_face_dict.keys():
                    user_image = face_recognition.load_image_file(key + "/" + key + ".jpg")
                    user_face_encoding = face_recognition.face_encodings(user_image)[0]

                    face_locations = face_recognition.face_locations(small_frame)
                    face_encodings = face_recognition.face_encodings(small_frame, face_locations)
                    for face_encoding in face_encodings:
                        match = face_recognition.compare_faces([user_face_encoding], face_encoding)
                        status = "Unknown"

                        if match[0]:
                            status = "Success"
                            print(status + " : "+ key)
                            webbrowser.open_new_tab("http://172.20.10.8:5000/mirror/"+key)
                            return True
                        else:
                            print(status)
                            break;

                        face_names.append(status)

            process_this_frame = not process_this_frame
        except:
            e = sys.exc_info()[0]
            print("<p>Error: %s</p>" % e)
    return False

def captureImage(userName):
    global process_this_frame
    process_this_frame = False
    if os.path.isdir(userName):
        os.remove(userName + "/" + userName +".jpg")
        os.rmdir(userName)
        return "User Already Exists"
    video_capture = cv2.VideoCapture(0)
    name = userName
    captureImg = True
    count = 0;
    while captureImg:
        ret, img = video_capture.read()
        if count is 3:
            print("Image Captured")
            os.mkdir(name)
            cv2.imwrite(name + "/" + name + ".jpg", img)
            captureImg= False
        if count is not 3:
            count += 1
            print(count)
    video_capture.release()
    cv2.destroyAllWindows()
    process_this_frame = True
    return True

monitor()