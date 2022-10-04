"""
Copyright (C) 2022 Longhao Qian

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

-------------------------------------------------------------------------------

Simple SLAM with one cart with lidar and one landmark

"""

from re import X
from turtle import color
import numpy as np
import math
import matplotlib.pyplot as pl
from scipy.stats import binom

def MotionPredict(xk, vk, uk, deltaT):
    return xk + (vk + uk) * deltaT

def ObservationPredict(xk, xl, nk):
    return xl - xk + nk

def GetInput(xk, xk_1, deltaT):
    return (xk - xk_1) / deltaT

if __name__ == "__main__":
    # motion noise std:
    sigma_v = 0.1
    # observation noise std:
    sigma_n = 0.1
    # landmark position
    xl = 10
    # generate the trajectory of the cart
    numSteps = 1000
    v = 5
    t = np.linspace(0, 100, num=numSteps)
    deltaT = t[1] - t[0]
    xg = np.zeros_like(t)
    for i in range(t.size):
        xg[i] = v * math.cos(t[i])
    # calculate real input (the last one is not used)
    vk = np.zeros_like(t)
    for i in range(t.size - 1):
        vk[i] = GetInput(xg[i + 1], xg[i], deltaT)
    # generate observed input
    vkOb = np.zeros_like(vk)
    for i in range(t.size - 1):
        vkOb[i] = vk[i] + np.random.normal(0, sigma_v, 1)
    
    # generate observed measurements
    meas = np.zeros_like(t)
    for i in range(t.size - 1):
        meas[i] =  ObservationPredict(xg[i], xl, np.random.normal(0, sigma_n, 1))

    # now estimate the position and the landmark simultaneously
    
    pl.figure(1)
    pl.subplot(311)
    ax0 = pl.plot(t, xg)
    pl.xlabel("t(s)")
    pl.ylabel("x(m)")
    pl.grid(True)
    pl.subplot(312)
    ax1 = pl.plot(t, vk)
    ax1 = pl.scatter(t, vkOb, alpha=0.7, color="green", s=4)
    pl.xlabel("t(s)")
    pl.ylabel("v(m/s)")
    pl.grid(True)
    pl.subplot(313)
    ax2 = pl.scatter(t, meas, alpha=0.7, color="green", s=4)
    pl.xlabel("t(s)")
    pl.ylabel("meas(m)")
    pl.grid(True)
    pl.show()