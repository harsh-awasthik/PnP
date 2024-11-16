import numpy as np
from numpy.linalg import svd

# Known 3D points in the world (homogeneous coordinates)
world_points = np.array([
    [0, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 0, 1],
    [1, 1, 0, 1],
    [0, 0, 1, 1],
    [1, 0, 1, 1],
    [0, 1, 1, 1],
    [1, 1, 1, 1]
])

# Corresponding 2D image points (homogeneous coordinates)
image_points = np.array([
    [100, 100, 1],
    [200, 100, 1],
    [100, 200, 1],
    [200, 200, 1],
    [150, 150, 1],
    [250, 150, 1],
    [150, 250, 1],
    [250, 250, 1]
])

# Step 1: Construct matrix A using the 3D-2D correspondences
A = []
for i in range(len(world_points)):
    X, Y, Z, W = world_points[i]
    x, y, w = image_points[i]
    
    # First row for this correspondence (x equation)
    A.append([-X, -Y, -Z, -W, 0, 0, 0, 0, x * X, x * Y, x * Z, x * W])
    
    # Second row for this correspondence (y equation)
    A.append([0, 0, 0, 0, -X, -Y, -Z, -W, y * X, y * Y, y * Z, y * W])

A = np.array(A)

# Step 2: Apply SVD to solve for the projection matrix P
_, _, V = svd(A)

# Step 3: The last row of V (or last column of V^T) gives the solution
P = V[-1].reshape(3, 4)  # Reshape to form a 3x4 matrix

print("Estimated Camera Projection Matrix P:\n", P)
