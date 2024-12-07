import numpy as np

def rotational_to_euler(R):
    if np.isclose(R[2, 0], -1.0):
        pitch = np.pi / 2
        yaw = np.arctan2(R[0, 1], R[0, 2])
        roll = 0.0
    elif np.isclose(R[2, 0], 1.0):
        pitch = -np.pi / 2
        yaw = np.arctan2(-R[0, 1], -R[0, 2])
        roll = 0.0
    else:
        pitch = -np.arcsin(R[2, 0])
        roll = np.arctan2(R[2, 1] / np.cos(pitch), R[2, 2] / np.cos(pitch))
        yaw = np.arctan2(R[1, 0] / np.cos(pitch), R[0, 0] / np.cos(pitch))
    
    return yaw, pitch, roll