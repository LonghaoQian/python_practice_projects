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

import numpy as np
import matplotlib.pyplot as pl
from scipy.stats import binom
import env_setup as env
import numpy as np

if __name__ == '__main__':
    # load .csv file
    dataSetDirectory = "dataset/"
    fileName = "measurements.csv"
    dataset = env.CsvData(dataSetDirectory + fileName)
    print(dataset.labels)
    print(dataset.numOfColumns)
    print(dataset.nunOfRows)
    a = np.array([[1], [2], [3]])
    print(a)
    print(a.size)
    x = 1
    y = 2
    print(x+y)
    pl.figure(1)
    pl.plot([0, 1], [2, 3])
    pl.show()