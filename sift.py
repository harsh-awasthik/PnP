import numpy as np
import cv2


# for i in range(8):
img = cv2.imread(f'imgdata/img1.jpg', cv2.COLOR_BGR2GRAY)

# Define the rectangular region (x, y, width, height)
width = img.shape[1]
height = img.shape[0]
x, y, w, h = int(width/2), 0, int(width/2), int(height/2)  # Example coordinates for the rectangle

# Create a black mask of the same size as the img (all black)
mask = np.zeros(img.shape[:2], dtype=np.uint8)

# Create a white rectangle on the mask where you want the object to be visible
mask[y:y+h, x:x+w] = 255  # White rectangle inside the mask

# Apply the mask using bitwise AND operation
masked_img = cv2.bitwise_and(img, img, mask=mask)

sift = cv2.SIFT_create()

keypoints = sift.detect(masked_img, None)
for i, keypoint in enumerate(keypoints):
    x, y = keypoint.pt  # Get x, y coordinates of the keypoint
    # print(f"Keypoint {i}: Position = ({x:.2f}, {y:.2f})")

img = cv2.drawKeypoints(masked_img, keypoints, img, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imshow(f'sift_img/sift_img1.jpg', img)
cv2.waitKey(0)
