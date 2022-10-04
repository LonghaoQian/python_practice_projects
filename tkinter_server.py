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

a mock server to test tkinter plot function

"""
from socket import *
import sys
import time
import math
import os
from tkinter_socket_helper import *


if __name__ == "__main__":
    # start socket server
    port = 9999
    host = "127.0.0.1"
    try:
        s = socket(AF_INET, SOCK_STREAM)
        print("setup socket server")
    except error:
        sys.exit()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((host, port))
    # listen
    s.listen(5)
    conn, address = s.accept()
    client_struct = ClientStruct()
    server_struct = ServerStruct()

    index = int(0)
    t = 0
    deltat = 0.05
    id = -1
    currId = int(0)
    while True:
        print("awaiting client message...")
        client_data = conn.recv(1024)
        client_struct.unpack(client_data)
        # determine whether the message is quit
        print("client message is: " + client_struct.message)
        if client_struct.id == -1:
            print("server quitting...")
            break
        else:
            print("received client request, sending reply...")
            time.sleep(0.1)
            id = id + 1
            currId = int(index % 3)
            t = t + int(currId) / 3
            server_struct.id = id
            server_struct.index = currId
            server_struct.data = math.cos(5 * t)
            conn.sendall(server_struct.pack())
            print("reply sent. The content is: id "
                  + str(id)
                  + ", index is:"
                  + str(currId)
                  + ", data is:"
                  + str(server_struct.data))
            index = index + 1
    s.close()
