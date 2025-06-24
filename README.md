# 📂 PnP - Pose Estimation Toolkit

This document provides a detailed explanation of the modules implemented in the **PnP** repository.  
It covers object pose estimation using **Perspective-n-Point (PnP)**, feature matching with **SIFT**, **homography estimation**, and **camera calibration techniques** like **DLT** and **Zhang's Method**.

Use this as a reference to understand the complete workflow and the role of each component in the system.

---

## 📷 PnP (Perspective-n-Point) Automation

This module helps in **detecting the orientation and position of an object (like a gate)** using live camera input and estimating 3D pose using the PnP algorithm.

### 🛠️ Workflow Overview:
- First, the user manually selects a quadrilateral region (e.g., a gate) in the first frame.
- SIFT keypoints and descriptors are extracted from this region.
- In each subsequent frame:
  - Keypoints are matched using BFMatcher.
  - RANSAC is used to find a reliable homography between frames.
  - If enough inliers exist, `cv2.solvePnP()` is applied to estimate the camera's position relative to the selected object.

### 📌 What Each File Does:
- **`ransac.py`**: Handles initial image loading, feature detection, keypoint matching, homography estimation using RANSAC, and visualization.
- **`function.py`**: Contains helper functions to:
  - Select points on image (`get_four_points`, `get_n_points`)
  - Mask and draw quadrilateral regions
  - Convert rotation matrix to Euler angles
- **`solvepnp.py`**: Uses the detected region and known real-world object dimensions to:
  - Run `cv2.solvePnP()` on the matching points
  - Convert the rotation vector to Euler angles (yaw, pitch, roll)
  - Display both translation and orientation values over the live camera feed

### 🎯 Output:
- Live matching of detected region between frames.
- Estimated **yaw**, **pitch**, **roll**, and **translation (x, y)** vectors shown live.
- Transformed quadrilateral drawn on the moving frame.
- Terminal shows match accuracy percentage per frame.

### ❌ Limitation:
- Accuracy is highly dependent on good lighting, sufficient texture for keypoints, and precision in manual selection of points.
- If not enough matches or inliers are found, pose estimation will fail for that frame.

---

## 🔧 DLT and Camera Matrix Decomposition

This module helps us calculate the camera projection matrix using known 3D world points and their 2D image positions, and then decompose it into camera parameters.



### 📌 What it does:
- Takes 3D object coordinates and 2D image points.
- Normalizes the data for better accuracy.
- Uses SVD to calculate the projection matrix (DLT).
- Projects 3D points back to the image plane.
- Draws both actual and projected points on the image.
- Calculates the mean error of projection.
- Applies **RQ decomposition** to extract:
  - **K**: Camera Calibration Matrix (intrinsics)
  - **R**: Rotation Matrix
  - **T**: Translation Vector


### 🖼️ Output:
- `projected_points.jpg` with red (original) and blue (projected) dots.
- Projection matrix and error printed in the terminal.
- K, R, and T matrices displayed after decomposition.


### ❌ Limitation:
Although the DLT and decomposition code run successfully, they are **not giving reliable results in our case**.  
This is because DLT requires **very precise input measurements** (especially accurate 3D coordinates and image points).  
As a result, the method does **not estimate the object's distance from the camera accurately**, which is essential for our application.

---

## 🧠 SIFT Feature Detection and Matching

This module includes two uses of SIFT:
- Selecting strong feature points from an image.
- Matching features live using webcam frames and homography.



### 📌 What it does:
- Applies **SIFT** to detect feature points.
- In the first part, it selects and saves **6 strong, well-spaced keypoints** from a masked region in an image.
- In the second part, it uses **real-time webcam frames** to detect and match features with a selected region.
- Computes **homography** to transform the selected region across frames.
- Displays match accuracy and overlays matching area on the live video.


### 🖼️ Output:
- `selected6Poinnts.jpg`: Image with 6 labeled keypoints.
- `pointsdata.txt`: Coordinates of selected keypoints from image.
- Real-time SIFT matches and homography tracking via webcam.
- Accuracy of the match shown on the video feed.


### ✅ Use Case:
- Use the **static keypoint extraction** part when you need clean, stable feature points for calibration or matching.
- Use the **live matching with homography** for dynamic tracking and object detection in video.


### 📝 Note:
Both parts use SIFT but have **different goals** — one is offline and controlled, the other is real-time and interactive.

---

## 📷 Zhang's Camera Calibration Method

This module implements Zhang’s method to calibrate a camera using a series of checkerboard images. It follows a two-step approach: first collecting data (images), then performing calibration.


### 📌 What it does:
- Captures multiple images of a checkerboard from different angles and distances using a webcam.
- Detects inner corners of the checkerboard in each image using OpenCV.
- Defines the 3D world coordinates based on checkerboard layout and real-world square size.
- Computes:
  - Camera matrix (intrinsic parameters)
  - Distortion coefficients
  - Rotation vectors
  - Translation vectors


### 🖼️ Output:
- Camera Matrix: Printed as a 3×3 matrix representing focal lengths and optical centers.
- Distortion Coefficients: Printed as a vector describing lens distortion.
- Rotation and Translation Vectors: Printed for each calibration image.
- Checkerboard corners visualized on images during processing.


### ✅ Use Case:
This method is useful for accurately calibrating a camera to remove distortion and understand its internal geometry. It is widely used in 3D vision, robotics, and AR applications.


### 📝 Notes:
- The checkerboard used has 6 rows × 8 columns of inner corners.
- Each square is assumed to be 20 mm × 20 mm in size.
- Accuracy improves when the images are captured from different angles and distances.
- Capturing 15–20 well-framed images with clearly visible corners is recommended.

---
## 📁 Folder Structure
<pre>
PnP/
│
├── function.py
├── ransac.py
├── solvepnp.py
├── data/
│   ├── pointsdata.txt
│   └── selected6Points.jpg
├── RealsenseImages/
│   └── img0.jpg to img80.jpg
├── Calibration/
│   └── images/
│       └── img1.jpg ...
├── dlt.py, dlt_chatgpt.py
├── projected_points.jpg
├── workflow.md
├── README.md
└── ...
</pre>
