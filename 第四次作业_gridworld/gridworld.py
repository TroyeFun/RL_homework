import numpy as np
import random

gamma = 0.9

A = np.array([0, 1])
B = np.array([0, 3])

direct = np.array([[0, -1], [0, 1], [-1, 0], [1, 0]])

def goOut(x, y):
    if x == -1 or x == 5 or y == -1 or y == 5:
        return True
    return False

V = np.zeros([5, 5])
iteration = 1

while True:
    error = 0
    for x in range(5):
        for y in range(5):
            new_value = 0
            for d in direct:
                x1 = x + d[0]
                y1 = y + d[1]
                reward = 0
                if x == A[0] and y == A[1]:
                    reward = 10
                    x1 = 4
                    y1 = 1
                elif x == B[0] and y == B[1]:
                    reward = 5
                    x1 = 2
                    y1 = 3
                elif goOut(x1, y1):
                    reward = -1
                    x1 = x
                    y1 = y
                new_value += 0.25 * (reward + gamma * V[x1, y1])
            error += (new_value - V[x, y])**2
            V[x, y] = new_value
    if error <= 1e-4:
        print('Iteration: ', iteration)
        print(V)
        break
    iteration += 1

