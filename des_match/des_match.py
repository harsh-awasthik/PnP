import cv2
import numpy as np

# Load images
img1 = cv2.imread('../imgdata/img4.jpg', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('../imgdata/img5.jpg', cv2.IMREAD_GRAYSCALE)


# Define the rectangular region (x, y, width, height)
w1 = img1.shape[1]
h1 = img1.shape[0]
x, y, w, h = int(w1/2), 2*h1//5, int(w1/4.5), int(h1/4)   # Example coordinates for the rectangle

mask = np.zeros(img1.shape[:2], dtype=np.uint8)
mask[y:y+h, x:x+w] = 255  # White rectangle inside the mask

mask_img1 = cv2.bitwise_and(img1, img1, mask=mask)


# Define the rectangular region (x, y, width, height)
w2 = img2.shape[1]
h2 = img2.shape[0]
x, y, w, h = int(w2/2), 2*h2//5, int(w2/4), int(h2/4)  # Example coordinates for the rectangle

mask = np.zeros(img2.shape[:2], dtype=np.uint8)

# Create a white rectangle on the mask where you want the object to be visible
mask[y:y+h, x:x+w] = 255  # White rectangle inside the mask

mask_img2 = cv2.bitwise_and(img2, img2, mask=mask)


sift = cv2.SIFT_create()


kp1, d1 = sift.detectAndCompute(mask_img1, None)
kp2, d2 = sift.detectAndCompute(mask_img2, None)

bf = cv2.BFMatcher()
matches = bf.knnMatch(d1, d2, k=2)


# applying ratio test
good_matches = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good_matches.append(m)

good_matches = sorted(good_matches, key=lambda x: x.distance)

top_6_matches = good_matches[:7]

pts1 = np.float32([kp1[m.queryIdx].pt for m in top_6_matches])
pts2 = np.float32([kp2[m.trainIdx].pt for m in top_6_matches])

# Draw the matches (for visualization)
img_matches = cv2.drawMatches(img1, kp1, img2, kp2, top_6_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

print(pts1)
print("-----")
print(pts2)

cv2.imwrite(f'Match1-2.jpg',img_matches)