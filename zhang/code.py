import cv2
import os
import time

def capture_images(output_folder="images", num_images=60):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Start capturing video
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    print("Press 'q' to quit early.")

    count = 1
    time.sleep(2)
    while count <= num_images:
        time.sleep(0.5)
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        # Display the frame
        cv2.imshow("Capturing Images", frame)

        # Save the image
        img_name = os.path.join(output_folder, f"img{count}.jpg")
        cv2.imwrite(img_name, frame)
        print(f"Saved: {img_name}")

        count += 1

        # Wait briefly and allow quitting by pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Call the function
capture_images()
