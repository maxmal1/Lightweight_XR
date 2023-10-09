import numpy as np
import cv2
from mss import mss
import os
from helper import *
import math
import mediapipe as mp


def are_index_fingers_touching(hand1_landmarks, hand2_landmarks):
    # Define the landmarks for the index fingers of both hands
    index_finger_1 = hand1_landmarks[8]  # Index finger tip landmark for hand 1
    index_finger_2 = hand2_landmarks[8]  # Index finger tip landmark for hand 2

    # Calculate the Euclidean distance between the two index fingers
    distance = math.sqrt((index_finger_1.x - index_finger_2.x)**2 + (index_finger_1.y - index_finger_2.y)**2)

    # Define a threshold for considering them as touching (you can adjust this)
    touch_threshold = 0.03  # Adjust as needed

    # Check if the distance is below the threshold
    if distance < touch_threshold:
        return True
    else:
        return False

def index_dist(hand1_landmarks, hand2_landmarks):
    index_finger_1 = hand1_landmarks[8]  # Index finger tip landmark for hand 1
    index_finger_2 = hand2_landmarks[8]  # Index finger tip landmark for hand 2

    # Calculate the Euclidean distance between the two index fingers
    distance = math.sqrt((index_finger_1.x - index_finger_2.x)**2 + (index_finger_1.y - index_finger_2.y)**2)
    return distance

def stop_touch(hand1_landmarks, hand2_landmarks):
    index_finger_1 = hand1_landmarks[8]  # Index finger tip landmark for hand 1
    index_finger_2 = hand2_landmarks[8]  # Index finger tip landmark for hand 2
    thumb_finger_1 = hand1_landmarks[4]  # Thumb for hand1
    thumb_finger_2 = hand2_landmarks[4]  # Thumb for hand2
    
    distance1 = math.sqrt((index_finger_1.x - thumb_finger_1.x)**2 + (index_finger_1.y - thumb_finger_1.y)**2)
    distance2 = math.sqrt((index_finger_2.x - thumb_finger_2.x)**2 + (index_finger_2.y - thumb_finger_2.y)**2)

    # Define a threshold for considering them as touching (you can adjust this)
    touch_threshold = 0.03  # Adjust as needed
    
    if distance1 and distance2 < touch_threshold:
        return True
    else:
        return False
    


def vision():
    #Run commands to create more monitors
    os.system(r'cmd /c "plug_in\deviceinstaller64 enableidd 1"')
    
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=2,min_detection_confidence=0.2)

    # Initialize MediaPipe Drawing
    mp_drawing = mp.solutions.drawing_utils
        
    
    
    
    # Load the ArUco dictionary
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    
    # Create a video capture object (0 represents the default camera, change if necessary)
    cap = cv2.VideoCapture(0)

    # Initialize the MSS (monitor screen capture) object for the second monitor
    sct = mss()
    mon = sct.monitors[1]

    # Define the bounding box for the screen capture
    bounding_box = {
        "top": mon["top"] + 0,    # Adjust the top position as needed
        "left": mon["left"] + 0,  # Adjust the left position as needed
        "width": 3840,              # Adjust the width as needed
        "height": 2400,              # Adjust the height as needed
    }

    cv2.namedWindow('ArUco Marker Screen Capture', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('ArUco Marker Screen Capture', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    have_touched = False
    scale = 2
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        
        #testing resize
        frame = cv2.resize(frame, (3840, 2400))
        
        if not ret:
            break

        # Capture the screen of the second monitor
        sct_img = sct.grab(bounding_box)
        screen_capture = np.array(sct_img)

        # Convert the screen capture to RGB format
        screen_capture_rgb = cv2.cvtColor(screen_capture, cv2.COLOR_RGBA2RGB)
        

        # Process the frame to detect hands
        results = hands.process(frame)
        if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2:
            print("reading hands")
            landmarks1, landmarks2 = results.multi_hand_landmarks[0], results.multi_hand_landmarks[1]
            if have_touched:
                scale = index_dist(landmarks1.landmark, landmarks2.landmark)
                scale = scale*10
                print(scale)
            if are_index_fingers_touching(landmarks1.landmark, landmarks2.landmark):
                print("Index touching")
                have_touched = True
            if stop_touch(landmarks1.landmark, landmarks2.landmark):
                print("stop touching")
                have_touched = False
        
        # Detect ArUco markers in the camera frame

        corners, ids, _ = cv2.aruco.detectMarkers(frame, aruco_dict)

        if ids is not None:
            # Draw the detected markers
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            # Check if the marker with ID 0 is detected
            if 0 in ids:
                marker_index = list(ids).index(0)
                

                # Get the corners of the detected marker
                marker_corners = corners[marker_index][0]

                # Resize the screen capture to match the marker size
                    
                # Double the width and height of the resized image
                try:
                    
                    frame = resize_projection(marker_corners,screen_capture_rgb,frame, scale,"bot")

                except:
                    pass


        # Display the frame with the screen capture overlaid on the ArUco marker
        

            
            #mp_drawing.draw_landmarks(frame, landmarks1, mp_hands.HAND_CONNECTIONS)
            #mp_drawing.draw_landmarks(frame, landmarks2, mp_hands.HAND_CONNECTIONS)
        
        #frame_left1 = frame[:, 0:320+200]
        #frame_left2 = frame[:, 320-200:640]
        frame_left1 = frame[:,0:1920+1200]
        frame_left2 = frame[:,1920-1200:3840]
        combined_frame = cv2.hconcat([frame_left1, frame_left2])
        cv2.imshow('ArUco Marker Screen Capture', combined_frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    os.system(r'cmd /c "plug_in\deviceinstaller64 enableidd 0"')