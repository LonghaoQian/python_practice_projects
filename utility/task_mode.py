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

utility class containing multi-thread task class

"""

from multiprocessing import Lock
from typing import Any
from tkinter import *
import queue
import threading

"""
task queue class:
a queue struct containing task with priority.
"""


class Task:
    def __init__(self, priority: int, callback, para):
        self.priority = priority
        self.callback = callback
        self.para = para


class TaskQueue(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self._taskQueue = queue.Queue()
        self._taskOk = True
        self._lock = Lock()
        self.start()

    def PushTask(self, task: Task):
        self._lock.acquire()
        self._taskQueue.put(task)
        self._lock.release()

    def run(self):
        while self._taskOk:
            if self._taskQueue.empty():
                continue
            tmp = self._taskQueue.get()
            tmp.callback(tmp.para)

    def WaitForFinishing(self):
        while not self._taskQueue.empty():
            continue

    def EndTaskQueue(self):
        # end the task loop
        self.WaitForFinishing()
        self._lock.acquire()
        self._taskOk = False
        self._lock.release()
        self.join()


"""
task loop class:
loop execution supporting pause and resume
"""


class TaskLoop(threading.Thread):
    def __init__(self, initTask: Task, runTask: Task, stopTask: Task, pauseOnStart=False):
        super().__init__()
        self._taskOk = True
        self._taskPaused = pauseOnStart
        self._lock = Lock()
        self._initTask = initTask
        self._runTask = runTask
        self._stopTask = stopTask
        self._taskPara = runTask.para
        self._initTask.callback(self._initTask.para)
        self.start()

    def run(self):
        while self._taskOk:
            if self._taskPaused:
                continue
            self._runTask.callback(self._taskPara)

    def pause(self):
        self._lock.acquire()
        self._taskPaused = True
        self._lock.release()

    def resume(self):
        self._lock.acquire()
        self._taskPaused = False
        self._lock.release()

    def SetTaskPara(self, para):
        self._lock.acquire()
        self._taskPara = para
        self._lock.release()

    def EndLoop(self):
        self._lock.acquire()
        self._taskOk = False
        self._lock.release()
        self.join()
        self._stopTask.callback(self._stopTask.para)
