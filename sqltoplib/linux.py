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
import getopt
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
        pass

    def kill(self, pid):
        """
        Kil a mysql threads
        """
        try:
            self._sql.execute('kill ' + pid)
        except MySQLdb.OperationalError as e:
            raise processmanager.ProcessManagerError("Impossible to kill pid : " + str(pid))
   

