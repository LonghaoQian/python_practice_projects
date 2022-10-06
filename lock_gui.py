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

A python example for updating plots and tables in a GUI

"""

from cProfile import label
from turtle import numinput
import math
import matplotlib.pyplot as pl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import messagebox
from utility import *
from tkinter_socket_helper import *
from socket import *

S_TO_MS = 1000  # s to ms

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
            pl.xlabel("t(s)")
            pl.ylabel("distance(m)")
            line, = self.axes[-1].plot([], [], '-r')
            self.line.append(line)
        self.canvs = FigureCanvasTkAgg(self.fig1, root)
        self.canvs.get_tk_widget().place(x=xpos, y=ypos)

# the display window must run in the main thread

class Display:
    def __init__(self):
        self._root = Tk()
        self._root.geometry('1200x500')
        self._root.resizable(False, False)
        # init data
        self._deltat = 0.05
        self._dist = 0
        # init single axis
        self._plot = TKinterPlot(self._root, (8, 4.3), 300, 15, 0, 5, 1)
        # init label
        self._lockThreshold = 0.2
        self.InitLabel()
        # setup socket communication
        self.InitSocket()
        # setup closing function
        self._root.protocol("WM_DELETE_WINDOW", self.OnClosing)
        # start drawloop
        self._afterhandler = Any
        self.DrawFig()
        # start the mainloop
        self._root.mainloop()

    def InitLabel(self):
        self._distLabel = Label(self._root,
                                text="dist=0[m]",
                                bg="white",
                                font=("Helvetica", 20),
                                width=12,
                                height=3)
        self._distLabel.place(x=30,y=100)
        self._lockLable =Label(self._root,
                              text="locked",
                              bg="red",
                              font=("Helvetica", 20),
                              width=12,
                              height=3)
        self._lockLable.place(x=30,y=230)

    def InitSocket(self):
        # init as a socket client
        self.port = 9999
        self.host = "127.0.0.1"
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((self.host, self.port))
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        initTask = task_mode.Task(0, self.OnSocketInit, 0)
        runTask = task_mode.Task(0, self.OnGetResult, 0)
        stopTask = task_mode.Task(0, self.OnSocketStop, 0)
        self.sockeloop = task_mode.TaskLoop(initTask, runTask, stopTask)

    def OnSocketInit(self, para):
        pass

    def OnGetResult(self, para):
        client_struct = ClientStruct()
        client_struct.id = 0
        client_struct.message = "request distance"
        self.s.sendall(client_struct.pack())
        # wait for reply
        server_ply = self.s.recv(1024)
        # print data and index
        server_struct = ServerStruct()
        server_struct.unpack(server_ply)
        if server_struct.index == 0:
            self._dist = server_struct.data
        # update label

    def OnSocketStop(self, para):
        # send stop message
        client_struct = ClientStruct()
        client_struct.id = -1
        client_struct.message = "server exit"
        self.s.sendall(client_struct.pack())
        self.s.close()

    def OnClosing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.sockeloop.EndLoop()
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
        self._plot.xsq[index].AddData(self._plot.t[index], self._dist)
        res = self._plot.xsq[index].GetDataAndRange()
        # update x limit
        self._plot.axes[index].set_xlim(res[0], res[1])
        # update y limit
        self._plot.axes[index].axes.set_ylim(-2, 2)
        # update plot
        x = list()
        y = list()
        for data in res[2]:
            x.append(data[0])
            y.append(data[1])
        self._plot.line[index].set_xdata(x)
        self._plot.line[index].set_ydata(y)
        self._distLabel.config(text="dist="+str(round(self._dist, 2))+"[m]")
        if self._dist < self._lockThreshold:
            self._lockLable.config(text="unlocked",bg="green")
        else:
            self._lockLable.config(text="locked",bg="red")

    def DrawFig(self):
        self.UpdateCanvas(0)
        self._plot.canvs.draw()
        # incure next loop
        self._afterhandler = self._root.after(
            int(self._deltat * S_TO_MS), self.DrawFig)


if __name__ == "__main__":
    window = Display()