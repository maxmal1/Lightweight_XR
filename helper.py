import cv2
import numpy as np

def resize_projection(marker_corners, screen_capture_rgb, frame, scale, arg="center"):
    centroid = np.mean( marker_corners, axis=0)
    centered_shape_coordinates = marker_corners - centroid
    marker_corners = centered_shape_coordinates * scale + centroid
    
    
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
