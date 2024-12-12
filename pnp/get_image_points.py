import cv2

image = cv2.imread("C:/Users/harsh/Desktop/gate images/img1_Color.png")


selected_points = []

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN: 
        print(f"Point selected: ({x}, {y})")
        selected_points.append((x, y))
        text = f"({x}, {y})"
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, text, (x, y - 10), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Image", image)

cv2.imshow("Image", image)
cv2.setMouseCallback("Image", click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("imgpoints.jpg", image)
print("Selected Points:", selected_points)
'''

import cv2

def show_coordinates(event, x, y, flags, param):
    """Callback function to capture mouse click events and print coordinates."""
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordinates: x={x}, y={y}")

# Path to your image
image_path = 'C:/Users/harsh/Desktop/gate images/img1_Color.png'

# Load the image
image = cv2.imread(image_path)
if image is None:
    print("Error: Image not found or could not be loaded.")
    exit()

# Display the image in a window
cv2.imshow('Click on the image', image)

# Set the callback function for mouse events
cv2.setMouseCallback('Click on the image', show_coordinates)

# Wait for a key press or window close
cv2.waitKey(0)
cv2.destroyAllWindows()
'''