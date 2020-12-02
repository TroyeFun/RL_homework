import random
import numpy as np
import os
import math

gamma = 1.0
thrd = 1e-5
max_episode = 500
step_size = 0.02
method = 'MC'
true_V = np.array([1/6, 2/6, 3/6, 4/6, 5/6])

assert method in {'MC', 'TD'}

def print_log(episode, V, foutput):
    output = str(episode) + ':'
    for v in V:
        output += ' {:.4f}'.format(v)
    output += ' {:.4f}'.format(RMS(V))
    
    print(output)
    print(output, file=foutput)

def RMS(V):
    return math.sqrt(np.mean((true_V - V)**2))


if __name__ == '__main__':

    # initialize 
    V = np.ones((5,)) * 0.5

    if not os.path.exists('log'):
        os.makedirs('log')

    if method == 'MC':
        foutput = open('log/MC_alpha{}.txt'.format(step_size), 'w')
        episode = 1
        cnts = np.zeros((5,))
        while True:
            if episode > max_episode:
                break
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
                V[s] += step_size * (G - V[s])

            print_log(episode, V, foutput)

            delta = max(np.abs(V - old_V))
            if delta < thrd:
                break
            episode += 1
    else:
        foutput = open('log/TD_alpha{}.txt'.format(step_size), 'w')
        episode = 1
        cnts = np.zeros((5,))
        while True:
            if episode > max_episode:
                break
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
                current_index = new_index
            
            print_log(episode, V, foutput)

            delta = max(np.abs(V - old_V))
            if delta < thrd:
                break
            episode += 1



