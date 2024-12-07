from dlt import DLT 
from scipy.linalg import rq
import numpy as np

def normalisation(K):
    K = np.array(K)

    normalised_k = np.divide(K, K[2, 2])

    return normalised_k

def decompose_projection_matrix(P):
    P = np.array(P)

    M = P[:, :3]

    # Perform RQ decomposition on M
    K, R = rq(M)

    # Ensure K has positive diagonal (camera calibration matrix should have positive diagonal elements)
    T = np.diag(np.sign(np.diag(K)))
    K = np.dot(K, T)
    R = np.dot(T, R)

    # Extract the tangential coordinates (camera center)
    t = np.linalg.inv(K) @ P[:, 3]

    return normalisation(K), R, t


def qr():
    Projection_matrix, err = DLT()

    # Applying decomposition
    K, R, T = decompose_projection_matrix(Projection_matrix.reshape(3, 4))

    return K, R, T


if __name__ == "__main__":
    # Applying decomposition
    K, R, T = qr()

    print("Camera Calibration Matrix")
    print(K)
    print("----------------------------")

    print("Rotational Matrix")
    print(R)
    print("----------------------------")

    print("Transitional Matrix")
    print(T)
    print("----------------------------")
