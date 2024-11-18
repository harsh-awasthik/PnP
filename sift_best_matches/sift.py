import numpy as np
import cv2


# for i in range(8):
img = cv2.imread(f'../imgdata/img4.jpg', cv2.COLOR_BGR2GRAY)

# Define the rectangular region (x, y, width, height)
w1 = img.shape[1]
h1 = img.shape[0]
x, y, w, h = int(w1/2) + 25, 2*h1//5 + 35, int(w1/4.5) - 55, int(h1/3) 


mask = np.zeros(img.shape[:2], dtype=np.uint8)


mask[y:y+h, x:x+w] = 255  # White rectangle inside the mask


masked_img = cv2.bitwise_and(img, img, mask=mask)

sift = cv2.SIFT_create()

keypoints,  descriptors = sift.detectAndCompute(masked_img, None)


keypoints = sorted(keypoints, key=lambda kp: kp.response, reverse=True)

# Filter keypoints based on spatial distance
selected_keypoints = []
distance_threshold = 20 # Minimum distance between keypoints

for kp in keypoints:
    if all(np.linalg.norm(np.array(kp.pt) - np.array(sel_kp.pt)) > distance_threshold for sel_kp in selected_keypoints):
        selected_keypoints.append(kp)
    if len(selected_keypoints) >= 6:  # Stop after selecting 6 keypoints
        break

with open("pointsdata.txt", "w") as file:
    file.write("s.no,x,y\n")
    for i, kp in enumerate(selected_keypoints):
        center = tuple(map(int, kp.pt))
        radius = 6      
        cv2.circle(img, center, radius, (0, 255, 0), 2) 
        cv2.putText(img, str(i+1), tuple(map(int, kp.pt)), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 4)

        file.write(f"{i+1},{kp.pt[0]},{kp.pt[1]}\n")

# img = cv2.drawKeypoints(masked_img, selected_keypoints, img, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imwrite('selected6Poinnts.jpg', img)

