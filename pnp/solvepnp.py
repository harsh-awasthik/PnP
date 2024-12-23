import numpy as np
import cv2
from function import rotational_to_euler

camera_matrix = np.array([[675.537322,0.000000,311.191300],
                          [0.000000,677.852071,221.610964],
                          [0, 0, 1]])



dist_coeffs = np.zeros((4, 1)) #Assuming no distortion

image_points = np.array([(404, 96), (1015, 153), (413, 561), (951, 519)], dtype=np.float32)

object_points = np.array([[0, 0, 0],
                          [42, 0, 0],
                          [0, 0, -29],
                          [0, 42, -29]], dtype=np.float32)



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
