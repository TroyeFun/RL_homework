#!/usr/bin/env python
# coding=utf-8

import numpy as np
np.set_printoptions(precision=1, linewidth=200)
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


V_path = 'log/V-4.npy'
pi_path = 'log/pi-4.npy'

V = np.load(V_path)
pi = np.load(pi_path)

print('V table:')
print(V)

print('pi table:')
print(pi)

pi_image = (pi + 5) * 20
cv2.imwrite('log/pi.png', pi_image)

x = np.array(range(21))
y = np.array(range(21))
x_mesh, y_mesh = np.meshgrid(x, y, indexing='ij')
z_mesh = V
fig=plt.figure()
sub=fig.add_subplot(111,projection='3d')#3d表示三维图像
sub.plot_surface(x_mesh,y_mesh,z_mesh,cmap=plt.cm.plasma)

plt.xticks([0, 10, 20])
plt.yticks([0, 10, 20])

sub.set_xlabel(r'$x1$')
sub.set_ylabel(r'$x2$')
sub.set_zlabel(r'$V$')

plt.savefig('log/V.png')
#plt.show()

