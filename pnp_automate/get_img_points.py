import cv2

image = cv2.imread("RealsenceImages/img0.jpg")


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