#!/usr/bin/env python
# coding=utf-8

import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np

MC_alphas = [0.005, 0.01]  # for rms plot
TD_alphas = [0.005, 0.01, 0.05]
dot_type = ['-', '--', '-.', ':']

TD_alpha = 0.01  # for V plot
plot_episodes = [1, 100, 500]
colors = ['r', 'g', 'b']


# plot rms 
def plot_rms():
    plt.clf()
    plt.xlabel('Episodes')
    plt.ylabel('RMS error')
    for i, alpha in enumerate(MC_alphas):
        flog = open('log/MC_alpha{}.txt'.format(alpha), 'r')

        episodes = []
        rmss = []
        for line in flog.readlines():
            line = line.strip().split(' ')
            episode, rms = float(line[0].strip(':')), float(line[-1])
            episodes.append(episode)
            rmss.append(rms)
        x_new = np.linspace(min(episodes), max(episodes), 50)
        y_smooth = make_interp_spline(np.array(episodes), np.array(rmss))(x_new)
        
        plt.plot(x_new, y_smooth, dot_type[i], label='MC α={}'.format(alpha), color='r')

    for i, alpha in enumerate(TD_alphas):
        flog = open('log/TD_alpha{}.txt'.format(alpha), 'r')

        episodes = []
        rmss = []
        for line in flog.readlines():
            line = line.strip().split(' ')
            episode, rms = float(line[0].strip(':')), float(line[-1])
            episodes.append(episode)
            rmss.append(rms)
        x_new = np.linspace(min(episodes), max(episodes), 50)
        y_smooth = make_interp_spline(np.array(episodes), np.array(rmss))(x_new)
        
        plt.plot(x_new, y_smooth, dot_type[i], label='TD α={}'.format(alpha), color='b')
    plt.legend(loc='upper right')
    plt.savefig('log/rms.png')

def plot_V():
    plt.clf()
    x = np.array([0, 1, 2, 3, 4])
    init_V = np.array([0.5]*5)
    true_V = np.array([1/6, 2/6, 3/6, 4/6, 5/6])
    
    plt.plot(x, init_V, color='yellow', marker='.', label='Episode 0')
    plt.plot(x, true_V, color='black', marker='.', label='True values')

    flog = open('log/TD_alpha{}.txt'.format(TD_alpha), 'r')
    for line in flog.readlines():
        line = line.strip().split(' ')
        episode, V = int(line[0].strip(':')), list(map(float, line[1:6]))
        if episode in plot_episodes:
            plt.plot(x, np.array(V), color=colors[plot_episodes.index(episode)], marker='.', label='Episode {}'.format(episode))
    
    plt.xlabel('State')
    plt.ylabel('Value')
    plt.legend()
    plt.savefig('log/value.png')
    

if __name__ == '__main__':
    plot_rms()
    plot_V()
    



