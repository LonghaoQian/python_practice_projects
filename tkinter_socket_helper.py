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

contains helper data structures and functions

"""

import struct

RECV_BUFF_SIZE = 128


class ClientStruct:
    def __init__(self):
        self.id = 0
        self.message = ""
        self._fmt = "<i" + str(RECV_BUFF_SIZE) + "s"

    def pack(self):
        res = self.message.ljust(RECV_BUFF_SIZE, "\0")
        return struct.pack(
            self._fmt,
            self.id,
            res.encode("utf-8")
        )

    def unpack(self, client_data):
        self.id, self.message = struct.unpack(
            self._fmt, client_data)
        self.message = self.message.decode("utf-8")

class ServerStruct:
    def __init__(self):
        self.id = 0
        self.index = 0
        self.data = 0
        self._fmt = "<iId"

    def pack(self):
        return struct.pack(
            self._fmt,
            self.id,
            self.index,
            self.data
        )

    def unpack(self, server_data):
        self.id, self.index, self.data = struct.unpack(
            self._fmt, server_data)
