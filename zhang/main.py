import cv2
import numpy as np
import os
import glob

# Defining the dimensions of checkerboard
CHECKERBOARD = (7, 9) # ---- change  6 row 8 column
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Creating vector to store vectors of 3D points for each checkerboard image
objpoints = []
# Creating vector to store vectors of 2D points for each checkerboard image
imgpoints = [] 


# Defining the world coordinates for 3D points
square_size = 20  # Size of one square in mm   -------- change
objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2) * square_size
prev_img_shape = None


# Extracting path of individual image stored in a given directory
images = glob.glob('./images/*.jpg')
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    # If desired number of corners are found in the image then ret = true
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH+
    	cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)
    
    """
    If desired number of corner are detected,
    we refine the pixel coordinates and display 
    them on the images of checker board
    """

    if ret == True:
        objpoints.append(objp)
        # refining pixel coordinates for given 2d points.
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2,ret)
    else:
        print("Error")
    
    cv2.imshow('img', img)  
    cv2.waitKey(0) 
    
cv2.destroyAllWindows()


"""
Performing camera calibration by 
passing the value of known 3D points (objpoints)
and corresponding pixel coordinates of the 
detected corners (imgpoints)
"""
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

# Print Camera Matrix  ----- change
print("Camera Matrix:\n") 
print("\n".join(["\t".join([f"{value: .6f}" for value in row]) for row in mtx]))

# Print Distortion Coefficients ----- change
print("\nDistortion Coefficients:\n")
print(", ".join([f"{value: .6f}" for value in dist[0]]))

# Print Rotation Vectors ----- change
print("\nRotation Vectors (rvecs):\n")
for i, rvec in enumerate(rvecs, 1):
    print(f"rvec {i}: " + ", ".join([f"{value: .6f}" for value in rvec.ravel()]))

# Print Translation Vectors ----- change
print("\nTranslation Vectors (tvecs):\n")
for i, tvec in enumerate(tvecs, 1):
    print(f"tvec {i}: " + ", ".join([f"{value: .6f}" for value in tvec.ravel()]))