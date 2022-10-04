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

A python example for updating plots in a GUI

"""

from turtle import numinput
import math
import matplotlib.pyplot as pl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import messagebox
from utility import *

S_TO_MS = 1000 # s to ms

class TKinterPlot:
    def __init__(self, root, size, xpos, ypos, start, span, numPlots):
        self.fig1 = pl.figure(figsize=size)
        self.t = list()
        self.xsq = list()
        self.axes = list()
        self.line = list()
        for i in range(0, numPlots):
            self.t.append(0)
            self.xsq.append(DynamicTimeHistory(start, span))
            self.axes.append(self.fig1.add_subplot(numPlots, 1, i + 1))
            self.axes[-1].grid(True)
            line, = self.axes[-1].plot([], [], '-r')
            self.line.append(line)
        self.canvs = FigureCanvasTkAgg(self.fig1, root)
        self.canvs.get_tk_widget().place(x=xpos, y=ypos)

# the display window must run in the main thread
class Display:
    def __init__(self):
        self._root=Tk()
        self._root.geometry('1500x900')
        self._root.resizable(False, False)
        # init data
        self._deltat = 0.1
        # position of Axis
        self.numOfAxis = 3
        # init axis
        self._plot = TKinterPlot(self._root, (9, 8.5), 450, 15, 0, 5, 3)
        # setup socket communication
        self.InitSocket()
        # setup closing function
        self._root.protocol("WM_DELETE_WINDOW", self.OnClosing)
        # start drawloop
        self._afterhandler = Any
        self.DrawFig()
        # start the mainloop
        self._root.mainloop()

    def InitSocket(self):
        pass

    def OnClosing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # cancel the after funtion
            self._root.after_cancel(self._afterhandler)
            # close the figure (otherwise the program will stuck)
            pl.close('all')
            # then destory the window
            self._root.destroy()
        else:
            self._root.after(self._deltat, self.DrawFig())

    def UpdateCanvas(self, index):
        self._plot.t[index] = self._plot.t[index] + self._deltat
        # update limit
        self._plot.xsq[index].AddData(self._plot.t[index],
                                      math.cos(5 * self._plot.t[index]))
        res = self._plot.xsq[index].GetDataAndRange()
        self._plot.axes[index].set_xlim(res[0], res[1])
        self._plot.axes[index].axes.set_ylim(-2, 2)
        # update plot
        x = list()
        y = list()
        for data in res[2]:
            x.append(data[0])
            y.append(data[1])
        self._plot.line[index].set_xdata(x)
        self._plot.line[index].set_ydata(y)

    def DrawFig(self):
        self.UpdateCanvas(0)
        self.UpdateCanvas(1)
        self.UpdateCanvas(2)
        self._plot.canvs.draw()
        # incure next loop
        self._afterhandler = self._root.after(int(self._deltat * S_TO_MS), self.DrawFig)

if __name__ == "__main__":
    window = Display()