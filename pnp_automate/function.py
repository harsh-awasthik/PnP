import cv2
import numpy as np
import os
import time



def get_four_points(image):
    points = []

    def mouse_callback(event, x, y, flags, param):
        # Record a point on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))
            print(f"Point {len(points)} selected: ({x}, {y})")
            # Draw the point on the image
            cv2.circle(temp_image, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow("Select 4 Points", temp_image)

    # Load the image
    temp_image = image.copy()
    
    cv2.imshow("Select 4 Points", temp_image)
    cv2.setMouseCallback("Select 4 Points", mouse_callback)

    # Wait until 4 points are selected
    while len(points) < 4:
        cv2.waitKey(1)

    cv2.destroyAllWindows()
    return points

def get_n_points(n, image):
    points = []

    def mouse_callback(event, x, y, flags, param):
        # Record a point on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))
            print(f"Point {len(points)} selected: ({x}, {y})")
            # Draw the point on the image
            cv2.circle(temp_image, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow("Select 4 Points", temp_image)

    # Load the image
    temp_image = image.copy()
    
    cv2.imshow("Select 4 Points", temp_image)
    cv2.setMouseCallback("Select 4 Points", mouse_callback)

    # Wait until 4 points are selected
    while len(points) < n:
        cv2.waitKey(1)

    cv2.destroyAllWindows()
    return points

def draw_quadrilateral(image, points):
    pts = np.array(points, dtype=np.int32)
    
    # Create a blank mask of the same size as the image
    mask = np.zeros_like(image)
    
    # Fill the quadrilateral area on the mask
    cv2.fillPoly(mask, [pts], (255, 255, 255))
    
    # Apply the mask to the original image
    masked_image = cv2.bitwise_and(image, mask)
    
    # Draw the quadrilateral frame on the image
    cv2.polylines(masked_image, [pts], isClosed=True, color=(0, 255, 255), thickness=3)
    
    return masked_image

def rotational_to_euler(R):
    if np.isclose(R[2, 0], -1.0):
        pitch = np.pi / 2
        yaw = np.arctan2(R[0, 1], R[0, 2])
        roll = 0.0
    elif np.isclose(R[2, 0], 1.0):
        pitch = -np.pi / 2
        yaw = np.arctan2(-R[0, 1], -R[0, 2])
        roll = 0.0
    else:
        pitch = -np.arcsin(R[2, 0])
        roll = np.arctan2(R[2, 1] / np.cos(pitch), R[2, 2] / np.cos(pitch))
        yaw = np.arctan2(R[1, 0] / np.cos(pitch), R[0, 0] / np.cos(pitch))
    
    return yaw, pitch, roll