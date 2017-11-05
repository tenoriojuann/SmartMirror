import face_recognition
import cv2
import os
import webbrowser
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
class Facial:
    process_this_frame = True

    def __init__(self, path):
        self.database = DB(path)

    def get_all_email_images(self):

        emails = self.database.getEmail()
        user_image_dict = {}
        for email in emails:
            a_user_image = face_recognition.load_image_file(email[0] + "/" + email[0] + ".jpg")
            user_image_dict[email[0]] = a_user_image
        return user_image_dict

    def facial_authenticate(self):
        video_capture = cv2.VideoCapture(0)
        # Load a sample picture and learn how to recognize it.
        # emails = database.getEmail(database)
        # for email in emails:
        #     user_image = face_recognition.load_image_file(email[0] + "/"+ email[0] + ".jpg")
        #     user_face_encoding = face_recognition.face_encodings(user_image)[0]
        global process_this_frame
        while process_this_frame:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing

            # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Only process every other frame of video to save time
            if process_this_frame:
                user_face_dict = self.get_all_email_images()
                for key in user_face_dict.keys():
                    user_image = face_recognition.load_image_file(key + "/" + key + ".jpg")
                    user_face_encoding = face_recognition.face_encodings(user_image)[0]

                    face_locations = face_recognition.face_locations(frame)
                    face_encodings = face_recognition.face_encodings(frame, face_locations)
                    face_locations = []
                    face_names = []
                    for face_encoding in face_encodings:
                        # See if the face is a match for the known face(s)
                        match = face_recognition.compare_faces([user_face_encoding], face_encoding)
                        status = "Unknown"

                        if match[0]:
                            status = "Success"
                            print(status + " : " + key)
                            webbrowser.open_new_tab("http://172.20.10.8:5000/mirror/" + key)
                            # break
                        else:
                            print(status)
                            break

                        face_names.append(status)

            process_this_frame = not process_this_frame

            # # Display the results
            # for (top, right, bottom, left), name in zip(face_locations, face_names):
            #     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            #     top *= 4
            #     right *= 4
            #     bottom *= 4
            #     left *= 4
            #
            #     # Draw a box around the face
            #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            #
            #     # Draw a label with a name below the face
            #     cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            #     font = cv2.FONT_HERSHEY_DUPLEX
            #     cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            #
            # # Display the resulting image
            # cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #   break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()

    def captureImage(self, userName):
        global process_this_frame
        process_this_frame = False
        if os.path.isdir(userName):
            os.remove(userName + "/" + userName + ".jpg")
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
                captureImg = False
            if count is not 3:
                count += 1
                print(count)
        video_capture.release()
        cv2.destroyAllWindows()
        process_this_frame = True
        return True
