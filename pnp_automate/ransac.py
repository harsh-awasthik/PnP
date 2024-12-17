import cv2
import numpy as np
import os
sift = cv2.SIFT_create()
dir = "RealsenceImages/img"
MIN_MATCH = 10


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

import cv2
import numpy as np

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


# Load the images
img1 = cv2.imread(os.path.join("RealsenceImages/img0.jpg"), cv2.IMREAD_GRAYSCALE)  # First image
pts = get_four_points(img1)
img1 = draw_quadrilateral(img1, pts)
keypoints1, descriptors1 = sift.detectAndCompute(img1, None)


for i in range(1, 81):

    img2 = cv2.imread(os.path.join(f"RealsenceImages/img{i}.jpg"), cv2.IMREAD_GRAYSCALE)  # Second image
    keypoints2, descriptors2 = sift.detectAndCompute(img2, None)


    # Step 2: Match descriptors using BFMatcher
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)


    # Sort matches by distance
    good_matches = sorted(matches, key=lambda x: x.distance)

    matchesMask = np.zeros(len(good_matches)).tolist()
 
    if len(good_matches) > MIN_MATCH: 

        # Extract matched keypoints
        pts1 = np.float32([keypoints1[m.queryIdx].pt for m in good_matches])
        pts2 = np.float32([keypoints2[m.trainIdx].pt for m in good_matches])

        # Compute homography using RANSAC
        homography, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC, 5.0)

        # Calculate accuracy
        accuracy = float(mask.sum()) / mask.size
        print("accuracy: %d/%d (%.2f%%)" % (mask.sum(), mask.size, accuracy * 100))

        # Check if inliers are above the threshold
        if mask.sum() > MIN_MATCH:
            matchesMask = mask.ravel().tolist()  # Define matchesMask for valid matches

            # Draw a quadrilateral to visualize the transformation
            h, w = img1.shape[:2]
            pts = np.float32([[[0, 0]], [[0, h - 1]], [[w - 1, h - 1]], [[w - 1, 0]]])
            dst = cv2.perspectiveTransform(pts, homography)
            img2 = cv2.polylines(img2, [np.int32(dst)], True, (255, 0, 0), 3, cv2.LINE_AA)
        else:
            matchesMask = None  # Define matchesMask as None if insufficient inliers

        # Draw matches
        img_matches = cv2.drawMatches(
            img1, keypoints1, img2, keypoints2, good_matches, None,
            matchColor=(0, 255, 0), singlePointColor=(255, 0, 0),
            matchesMask=matchesMask,  # Safe to pass matchesMask even if None
            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )

        # Show the result
        cv2.imshow("Inlier Matches", img_matches)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print(f"Not enough matches found! Required: {MIN_MATCH}, Found: {len(good_matches)}")

cv2.destroyAllWindows()

