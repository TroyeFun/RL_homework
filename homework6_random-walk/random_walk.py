import random
import numpy as np
import os

gamma = 1.0
thrd = 1e-4
snapshot_epoch = 1
step_size = 0.05
method = 'MC'

assert method in {'MC', 'TD'}

def print_log(epoch, V, foutput):
    output = str(epoch) + ':'
    for v in V:
        output += ' {:.4f}'.format(v)
    print(output)
    print(output, foutput)

if __name__ == '__main__':

    # initialize 
    V = np.ones((5,)) * 0.5

    if not os.path.exists('log'):
        os.makedirs('log')

    if method == 'MC':
        foutput = open('log/MC.txt', 'w')
        epoch = 1
        cnts = np.zeros((5,))
        while True:
            current_index = 2
            experience = []
            while current_index not in [-1, 5]:
                action = 1 if random.random() < 0.5 else -1
                new_index = current_index + action
                if new_index == 5:
                    reward = 1
                else:
                    reward = 0
                experience.append((current_index, action, reward))
                current_index = new_index

            old_V = V.copy()
            G = 0

            experience.reverse()
            for s, a, r in experience:
                G = gamma * G + r
                cnts[s] += 1
                V[s] = V[s] + 1/cnts[s] * (G - V[s])

            print_log(epoch, V, foutput)

            delta = max(np.abs(V - old_V))
            if delta < thrd:
                break
            epoch += 1
    else:
        foutput = open('log/TD_alpha{}.txt'.format(step_size), 'w')
        epoch = 1
        cnts = np.zeros((5,))
        while True:
            old_V = V.copy()

            current_index = 2
            while current_index not in [-1, 5]:
                action = 1 if random.random() < 0.5 else -1
                new_index = current_index + action
                if new_index == 5:
                    reward = 1
                else:
                    reward = 0
                if new_index in [-1, 5]:
                    V[current_index] += step_size * (reward - V[current_index]) 
                else:
                    V[current_index] += step_size * (reward + gamma * V[new_index] - V[current_index])
            
            print_log(epoch, V, foutput)

            delta = max(np.abs(V - old_V))
            if delta < thrd:
                break
            epoch += 1

                





