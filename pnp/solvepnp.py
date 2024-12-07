import numpy as np
import cv2
from function import rotational_to_euler

camera_matrix = np.array([[106.83227657, -3.55675381, 901.58656603],
                          [0, 142.86282974, 525.60722677],
                          [0, 0, 1]])

dist_coeffs = np.zeros((4, 1)) #Assuming no distortion

image_points = np.array([(670, 424), (882, 426), (805, 527), (672, 604)], dtype=np.float32)

object_points = np.array([[8, 0, -4.5],
                          [8, 0, 5.5],
                          [0, 0, 0],
                          [0, 13.3, 4.5]], dtype=np.float32)



success, rvec, tvec = cv2.solvePnP(object_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_P3P)

print("Rotational Vectors: ")
print(rvec)
print("---------------------")

R, _ = cv2.Rodrigues(rvec)
print("Rotational Matrix:\n", R)
print("---------------------")

print("Euler Angles: ")
yaw, pitch, roll = rotational_to_euler(R)
print(f"Roll = {roll}")
print(f"Pitch = {pitch}")
print(f"Yaw = {yaw}")

print("Translational Vectors: ")
print(tvec)
print("----------------------")
