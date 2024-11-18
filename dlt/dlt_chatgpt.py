import numpy as np
from numpy.linalg import svd

# Known 3D points in the world (homogeneous coordinates)
world_points = np.array([
    [28, 52.3, -3, 1],
    [28, 52.3, 7, 1],
    [20, 66, 7, 1],
    [20, 59.5, 3, 1],
    [20, 52.3, 1.5, 1],
    [20, 52.3, -1.5, 1]
])

# Corresponding 2D image points (homogeneous coordinates)
image_points = np.array([
[666.4842529296875,613.1535034179688, 1],
[668.2966918945312,421.8475646972656, 1],
[886.0830078125,428.85101318359375, 1],
[847.1015625,497.61328125, 1],
[803.1819458007812,525.7821044921875, 1],
[803.1392211914062,553.331787109375, 1],
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
