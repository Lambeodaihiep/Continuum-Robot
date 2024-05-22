import numpy as np
import math

def circle_trajectory(center, radius):
    X, Y, Z = [], [], []
    t = np.arange(0,6.3,0.1)
    for i in range(len(t)):
        X.append(center[0] + radius * math.sin(t[i]))
        Y.append(center[1])
        Z.append(center[2] + radius * math.cos(t[i]))

    return X, Y, Z

# def square_trajectory(center, length):
