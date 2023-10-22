import cv2
import numpy as np
import screeninfo

def resize_projection(marker_corners, screen_capture_rgb, frame, scale, arg="center", location = False):
    marker_corners = marker_shape_to_monitor_shape(marker_corners, location)
    marker_corners = coordinate_scaling(marker_corners,scale, arg)
    image_width = screen_capture_rgb.shape[1]
    image_height = screen_capture_rgb.shape[0]
    image_corners = np.array([[0, 0], [image_width, 0], [image_width, image_height], [0, image_height]], dtype=np.float32)    
    matrix = cv2.getPerspectiveTransform(image_corners, marker_corners)
    image_mapped = cv2.warpPerspective(screen_capture_rgb, matrix, (frame.shape[1], frame.shape[0]))
    mask = np.zeros_like(frame, dtype=np.uint8)
    cv2.fillPoly(mask, [np.int32(marker_corners)], (255, 255, 255))  # White mask
    mask_inv = cv2.bitwise_not(mask)
    frame_with_overlay = cv2.bitwise_and(frame, mask_inv)
    frame_with_overlay = cv2.add(frame_with_overlay,image_mapped)
    return frame_with_overlay

def coordinate_scaling(marker_corners, scale, arg = "center"):
    #marker corners in the format bot left, bot right, top right, top left
    if arg == "center":
        centroid = np.mean( marker_corners, axis=0)
        centered_shape_coordinates = marker_corners - centroid
        marker_corners = centered_shape_coordinates * scale + centroid
        return marker_corners
    else:
        val = (marker_corners[0][1]+marker_corners[1][1])/2
        #print(marker_corners)
        centroid = np.mean( marker_corners, axis=0)
        centered_shape_coordinates = marker_corners - centroid
        marker_corners = centered_shape_coordinates * scale + centroid
        marker_corners[:,1] -= val - (marker_corners[0][1] + marker_corners[1][1])/2 #Works, but wow it 
        #took so long
        #print(marker_corners)
        #print(" ")
        
        return marker_corners

def marker_shape_to_monitor_shape(markers, location):
    # aruco markers return a square, so we need to reshape
    #the square to the correct dimentions of the user's screen
    
    monitor = screeninfo.get_monitors()[0]
    width, height = monitor.width, monitor.height
    ratio = width/height
    deltaX = (ratio-1) / 2.0
    
    scaled = np.float32([[-1,-1],[1,-1],[1,1],[-1,1]])
    scaled2 = np.float32([[-1 - deltaX,-1],[1 + deltaX,-1],[1 + deltaX,1],[-1 - deltaX,1]]) 
    if location:
        scaled2 = np.float32([[-13,-10],[-11,-10],[-11,-8],[-13,-8]])
    M = cv2.getPerspectiveTransform(scaled, markers)
    markers = cv2.perspectiveTransform(scaled2.reshape(1, -1, 2),M)
    return markers[0]