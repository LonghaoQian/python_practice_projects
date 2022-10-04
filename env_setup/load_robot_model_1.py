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

This file contains a series of robot model used for state estimation

"""

import math
import numpy as np

# bases class of a unicycle model with odometry
class RobotBaseUnicycle2D:
    def __init__(self, x0, y0, theta0):
        self._state = np.array([[x0], [y0], [theta0]])

    def MotionPredict(self, state, u, w, deltaT):
        ck = math.cos(state[2])
        sk = math.cos(state[2])
        res = state + deltaT * np.array([[ck, 0], [sk, 0], [0, 1]]) * (u + w)
        # angle wrapping
        res[2] = self.AngleWrap(res[2])
        return res

    def UpdateState(self, x, y, theta):
        self._state = np.array([[x], [y], [theta]])

    def GetState(self):
        return self._state

    def AssembleInput(self, v, omega):
        return np.array([[v], [omega]])

    def AssembleMotionNoise(self, wv, wo):
        return np.array([[wv], [wo]])

    def GetNumOfStates(self):
        return self._state.size

    def AngleWrap(self, angle):
        return np.arctan2(math.sin(angle), math.cos(angle))

class Landmark:
    def __init__(self):
        self.x = 0
        self.y = 0

# unicycle model + lidar
class RobotLidar(RobotBaseUnicycle2D):
    def __init__(self, x0, y0, theta0, d):
        super().__init__(x0, y0, theta0)
        self._d = d

    def ObservationPredict(self, state, para, n):
        x = state[0]
        y = state[1]
        theta = state[2]
        ck = math.cos(theta)
        sk = math.cos(theta)
        t2 = x - para.xl + self._d * ck
        t3 = y - para.yl + self._d * sk
        return np.array([[np.sqrt(t2**2 + t3**2)], [np.arctan2(-t3, -t2) - theta]]) + n
    
    def AssembleObservationNoise(self, nr, nb):
        return np.array([[nr], [nb]])