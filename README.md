# PnP Progress Log

## date
- Created `data.csv` with images and rotational/translational coordinates.

## date
- Applied SIFT to `imgdata` to create `sift_img`.
- Used BF matcher for keypoint matching in `des_match.py`.

## 13-11-24
- Chose 6 best SIFT-detected points for DLT.
- Used masking to ignore non-interest regions.

## 15-11-24
- Implemented `dlt_hardcode.py`.
- Found DLT fails on `img1.jpg` due to a single plane.

## 16-11-24
- Tested `img5.jpg` and `img4.jpg`, observed uneven SIFT matches.
- Fixed masking issues on `img4.jpg` and manually marked keypoints.
- Filtered keypoints with distances < 20px.
- Planned 3D point calculation for DLT in `dlt_hardcode.py`.

## 18-11-24
- Calculated 6 best 3D coordinates from SIFT.
- Applied DLT using `dlt_chatgpt.py` and a GitHub-sourced `dlt.py`.


## 20-11-2024
- Matched real points (red) with projected points (blue) on the image to check for errors.
- `NOT DONE` Identified minimal error and acknowledged the need to learn NumPy functions like `svd`, `concatenate`, `pinv`, and `flatten` used in the code.
- Understood the overall DLT process.

## 26-11-2024
- Confirmed that the DLT method was used successfully to estimate the projection matrix.
- Clarified the next steps involving 2D-3D correspondences and PnP camera pose estimation.
- Began exploring QR decomposition on the projection matrix to extract intrinsic parameters \( K \), rotation matrix \( R \), and translation vector \( T \).

## 27-11-2024
- Applied QR decomposition and verified that \( K \) is upper triangular and \( R \) is orthonormal.
- Normalized \( K \) by dividing by \( K[3,3] \) and calculated raw pitch and roll from \( R \).
- Determined \( T \) from the fourth column of the projection matrix and understood frame-of-reference differences.
- Planned to utilize OpenCV’s PnP algorithm (starting with P3P) for further computations.

## 29-11-2024
- Applied PnP algorithm to selected points in the original image, assuming zero distortion coefficients due to lack of calibration data.
- Converted rotation vectors to Euler angles using the Rodrigues method.
- Noted discrepancies in translation vectors and discussed potential issues with co-planar points.
- Concluded that co-planar points might lead to degenerate solutions.

## 04-12-2024
- Applied p3p on another image and taking non-coplaner points.
- Still receiving the errors.
- Identified that manual inaccuracies in point Calculation might be the root cause of errors.

## 10-12-2024
- Figured out that DLT was not feasible for calculating the calibration matrix, so decided to use the Zhang method instead.

## 11-12-2024
- The code for applying the Zhang method using the checkerboard function was written by Pragati.
- We (Harsh and Ammar) took 60 photos and applied the Zhang method to those images.
- Obtained the calibration matrix

## 12-12-2024
- We (Harsh and Ammar) applied the solvePnP function to obtain the rotational and translational vectors. `./pnp`
- These results are somewhat similar to what we calculated manually. The z-axis of the translational vector is similar the distance from the camera to the gate.
- he image can be seen at `./pnp/imgpoints.jpg`.