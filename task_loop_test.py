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

test task loop class

"""

from ctypes import set_errno
from socket import *
from typing import Any
from utility import task_mode
from tkinter_socket_helper import *
import time

port = 9999
host = "127.0.0.1"
s = socket(AF_INET, SOCK_STREAM)


def OnInit(para):
    s.connect((host, port))
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


def GetResult(para):
    client_struct = ClientStruct()
    client_struct.id = 0
    client_struct.message = "request distance"
    s.sendall(client_struct.pack())
    # wait for reply
    server_ply = s.recv(1024)
    # print data and index
    server_struct = ServerStruct()
    server_struct.unpack(server_ply)
    print("server message, id:"
          + str(server_struct.id)
          + " index: "
          + str(server_struct.index)
          + " data: "
          + str(server_struct.data))


def OnStop(para):
    # send stop message
    client_struct = ClientStruct()
    client_struct.id = -1
    client_struct.message = "server exit"
    s.sendall(client_struct.pack())
    s.close()


# start task loop as the client
if __name__ == '__main__':
    initTask = task_mode.Task(0, OnInit, 0)
    runTask = task_mode.Task(0, GetResult, 0)
    stopTask = task_mode.Task(0, OnStop, 0)
    sockeloop = task_mode.TaskLoop(initTask, runTask, stopTask)
    time.sleep(10)
    sockeloop.EndLoop()
