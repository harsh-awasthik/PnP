import cv2
import numpy as np

# Load the image (ensure to replace 'your_image.jpg' with your actual image path)
image = cv2.imread(f'imgdata/img1.jpg')

# Define the rectangular region (x, y, width, height)
width = image.shape[1]
height = image.shape[0]
x, y, w, h = int(width/2), 0, int(width/2), int(height/2)  # Example coordinates for the rectangle

# Create a black mask of the same size as the image (all black)
mask = np.zeros(image.shape[:2], dtype=np.uint8)

# Create a white rectangle on the mask where you want the object to be visible
mask[y:y+h, x:x+w] = 255  # White rectangle inside the mask

# Apply the mask using bitwise AND operation
masked_image = cv2.bitwise_and(image, image, mask=mask)

# Show the original and the masked images
cv2.imshow('Original Image', image)
cv2.imshow('Masked Image', masked_image)

# Wait for a key press and close windows
cv2.waitKey(0)
cv2.destroyAllWindows()
