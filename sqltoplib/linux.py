#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Patrick Charron
# Email : patrick.charron.pc@gmail.com
# Description : SQL process viewer
#  
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
sqloptlib is a library to manipulate and get sql server process
"""
import datetime
import re
import platform
import time

import processmanager
import process

try: #Try to import psutil library
    import psutil
except ImportError:
     raise processmanager.ProcessManagerError("linux backend not disponible") 

class Process(object):
    """
    A process class
    """
    def __init__(self, pid=0, user=None, host=None, state=None, time=0, info=None):
        self._pid = pid
        self._user = user
        self._host = host
        self._state = state
        self._time = time
        self._info = info

    @property
    def pid(self):
        """
        Get process pid
        """
        return self._pid
    @pid.setter
    def pid(self, value):
        """
        Set process pid
        """
        self._pid = value

    @property
    def user(self):
        """
        Get user running process
        """
        return self._user
    @user.setter
    def user(self, value):
        """
        Set user running process
        """
        self._user = value

    @property
    def host(self):
        """
        Get host
        """
        return self._host
    @host.setter
    def host(self, value):
        """
        Set host
        """
        self._host = value

    @property
    def db(self):
        """
        Get database name
        """
        return self._db
    @db.setter
    def db(self, value):
        """
        Set database name
        """
        self._db = value

    @property
    def state(self):
        """
        Get process state
        """
        return self._state
    @state.setter
    def state(self, value):
        """
        Set process state
        """
        self._state = value

    @property
    def time(self):
        """
        Get process running time
        """
        return self._time
    @time.setter
    def time(self, value):
        """
        Set process running time
        """
        self._time = value

    @property
    def info(self):
        """
        Get info
        """
        return self._info
    @info.setter
    def info(self, value):
        """
        Set info
        """
        self._info = value

class ProcessManager(processmanager.ProcessManager):
    """
    A class to manipulate and get sql server process
    """
    def __init__(self, user, host, password, port):
        processmanager.ProcessManager.__init__(self, user, host, password, port)
        self.BACKEND = "linux"
        
    def refresh(self):
        """
        Refresh sql information. Including uptime and the list of running process
        """
        linux_process = psutil.get_process_list()
        all_process = []
        for pr in linux_process:
            info = pr.name + " " + " ".join(pr.cmdline)
            p = process.Process(pr.pid, pr.username, "localhost", "None", "s", int(pr.create_time), info)
            all_process.append(p)
        if len(self._history) > self._max_history:
            self._history.pop(0)
            self._history.append(self._process)
        else:
            self._history.append(self._process)
        self._process = all_process
        f = open("/proc/uptime")
        proc_uptime = float(f.read().split()[0])
        self._uptime = str(datetime.timedelta(seconds = int(proc_uptime)))
        self._version = platform.release()

    def connect(self):
        self._is_online = True

    def kill(self, process, signal):
        process = psutil.Process(process.pid)
        process.send_signal(signal)
        
    def set_nice(self, process, nice):
        process = psutil.Process(process.pid)
        process.set_nice(nice)
   
