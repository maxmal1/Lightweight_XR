from pyuac import main_requires_admin
import numpy as np
import cv2
from mss import mss
import subprocess
import os

@main_requires_admin
def main():
    #Run commands to create more monitors
    #os.system(r'cmd /c "cd C:\Users\max\Downloads\usbmmidd_v2\usbmmidd_v2" & "deviceinstaller64 enableidd 1"')
    os.system(r'cmd /c "C:\Users\max\Downloads\usbmmidd_v2\usbmmidd_v2\deviceinstaller64 enableidd 1"')

    # Define the command as a list of strings


    # Load the ArUco dictionary
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

    # Create a video capture object (0 represents the default camera, change if necessary)
    cap = cv2.VideoCapture(0)

    # Initialize the MSS (monitor screen capture) object for the second monitor
    sct = mss()
    mon = sct.monitors[2]

    # Define the bounding box for the screen capture
    bounding_box = {
        "top": mon["top"] + 100,    # Adjust the top position as needed
        "left": mon["left"] + 100,  # Adjust the left position as needed
        "width": 1000,              # Adjust the width as needed
        "height": 1000,              # Adjust the height as needed
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
                
                """screen_capture_resized = cv2.resize(screen_capture_rgb, (int(marker_corners[2][0] - marker_corners[0][0]),
                                                                        int(marker_corners[2][1] - marker_corners[0][1])))

                # Replace the region of interest (ROI) with the resized screen capture
                
                frame[int(marker_corners[0][1]):int(marker_corners[2][1]),
                    int(marker_corners[0][0]):int(marker_corners[2][0])] = screen_capture_resized"""
                    
                # Double the width and height of the resized image
                new_width = int(2 * (marker_corners[2][0] - marker_corners[0][0]))
                new_height = int(2 * (marker_corners[2][1] - marker_corners[0][1]))
                screen_capture_resized = cv2.resize(screen_capture_rgb, (new_width, new_height))

                # Calculate the new coordinates for replacing the region of interest (ROI)
                new_x1 = int(marker_corners[0][0] - (new_width - (marker_corners[2][0] - marker_corners[0][0])) / 2)
                new_x2 = new_x1 + new_width
                new_y1 = int(marker_corners[0][1] - (new_height - (marker_corners[2][1] - marker_corners[0][1])) / 2)
                new_y2 = new_y1 + new_height

                # Replace the region of interest (ROI) with the resized screen capture
                frame[new_y1:new_y2, new_x1:new_x2] = screen_capture_resized


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

if __name__ == "__main__":
    main()