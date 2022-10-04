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

utility class for plot dynamic time history

"""

import queue

class DynamicTimeHistory:
    def __init__(self, xStart, xRange):
        self._xRange = xRange
        self._xStart = xStart
        self._xEnd = self._xStart + self._xRange
        self._data = queue.Queue()
    
    def AddData(self, x, y):
        # update range first
        if x > self._xEnd:
            self._xEnd = x
            self._xStart = self._xEnd - self._xRange
        # add current element to buffer
        self._data.put((x, y))
        # remove excess elements
        index = self._data.qsize() - 1
        while (self._data.queue[index][0] >= self._xStart) and (index >= 0):
            index = index - 1

        if (index - 1) < 0:
            return
        # remove excess elements
        for _ in range(0, index):
            self._data.get()

    def GetDataAndRange(self):
        return self._xStart, self._xEnd, self._data.queue