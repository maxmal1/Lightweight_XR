import numpy as np
import cv2


def resize_projection(marker_corners,screen_capture_rgb,frame,scale, arg = "center"):
    new_width = int(scale * (marker_corners[2][0] - marker_corners[0][0]))
    new_height = int(scale * (marker_corners[2][1] - marker_corners[0][1]))
    screen_capture_resized = cv2.resize(screen_capture_rgb, (new_width, new_height))
    
    #screen_capture_resized = cv2.resize(screen_capture_rgb, (new_width, new_height))

    # Calculate the new coordinates for replacing the region of interest (ROI)
    if arg == "center":
        x_div = 2
        y_div = 2
    if arg == "bottom":
        x_div = 2
        y_div = 1
    
    new_x1 = int(marker_corners[0][0] - (new_width - (marker_corners[2][0] - marker_corners[0][0])) / x_div)
    new_x2 = new_x1 + new_width
    new_y1 = int(marker_corners[0][1] - (new_height - (marker_corners[2][1] - marker_corners[0][1])) / y_div)
    new_y2 = new_y1 + new_height
    
    # Define the dimensions of the frame
    frame_height, frame_width, _ = frame.shape

    # Calculate the new coordinates for cropping
    crop_x1 = max(0, new_x1)
    crop_x2 = min(frame_width, new_x2)
    crop_y1 = max(0, new_y1)
    crop_y2 = min(frame_height, new_y2)

    # Perform the cropping
    cropped_screen_capture = screen_capture_resized[crop_y1 - new_y1:crop_y2 - new_y1, crop_x1 - new_x1:crop_x2 - new_x1]


    # Create a mask to place the cropped screen capture back onto the frame
    mask = np.zeros_like(frame)
    frame[crop_y1:crop_y2, crop_x1:crop_x2] = np.zeros_like(cropped_screen_capture)
    mask[crop_y1:crop_y2, crop_x1:crop_x2] = cropped_screen_capture

    # Add the masked screen capture to the frame
    
    frame += mask

    # Replace the region of interest (ROI) with the resized screen capture
    return frame