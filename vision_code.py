import numpy as np
import cv2
from mss import mss
import os
from helper import *

def vision():
    #Run commands to create more monitors
    os.system(r'cmd /c "plug_in\deviceinstaller64 enableidd 1"')

    # Define the command as a list of strings


    # Load the ArUco dictionary
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

    # Create a video capture object (0 represents the default camera, change if necessary)
    cap = cv2.VideoCapture(1)

    # Initialize the MSS (monitor screen capture) object for the second monitor
    sct = mss()
    mon = sct.monitors[3]

    # Define the bounding box for the screen capture
    bounding_box = {
        "top": mon["top"] + 0,    # Adjust the top position as needed
        "left": mon["left"] + 0,  # Adjust the left position as needed
        "width": 1050,              # Adjust the width as needed
        "height": 900,              # Adjust the height as needed
    }

    cv2.namedWindow('ArUco Marker Screen Capture', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('ArUco Marker Screen Capture', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        if not ret:
            break

        # Capture the screen of the second monitor
        sct_img = sct.grab(bounding_box)
        screen_capture = np.array(sct_img)

        # Convert the screen capture to RGB format
        screen_capture_rgb = cv2.cvtColor(screen_capture, cv2.COLOR_RGBA2RGB)

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
                    
                    frame = resize_projection(marker_corners,screen_capture_rgb,frame, 2)

                except:
                    pass


        # Display the frame with the screen capture overlaid on the ArUco marker
        
        frame_left1 = frame[:, 0:320+200]
        frame_left2 = frame[:, 320-200:640]
        combined_frame = cv2.hconcat([frame_left1, frame_left2])
        cv2.imshow('ArUco Marker Screen Capture', combined_frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    os.system(r'cmd /c "C:\Users\max\Downloads\usbmmidd_v2\usbmmidd_v2\deviceinstaller64 enableidd 0"')