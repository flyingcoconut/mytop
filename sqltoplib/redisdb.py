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

import processmanager
import process

try: #Try to import MySQLdb library
    import redis
except ImportError:
     raise processmanager.ProcessManagerError("redisdb backend not disponible")

class ProcessManager(processmanager.ProcessManager):
    """
    A class to manipulate and get sql server process
    """
    def __init__(self, user="root", host="localhost", password=None, port=3306):
        processmanager.ProcessManager.__init__(self, user, host, password, port)
        self.BACKEND = "redisdb"
        
    def refresh(self):
        """
        Refresh sql information. Including uptime and the list of running process
        """
        try:
            redis_process = self._sql.client_list()
        except:
            raise processmanager.ProcessManagerError("Could not retieve process")
        all_process = []
        try:
            for row in redis_process:     
                p = process.Process(1, "", row["addr"].split(':')[0], row["db"], row["flags"], row["age"], row["cmd"])
                all_process.append(p)
        except all as e:
            print e
            pass
        if len(self._history) > self._max_history:
            self._history.pop(0)
            self._history.append(self._process)
        else:
            self._history.append(self._process)
        self._process = all_process
        try:
            redis_stats = self._sql.info()
            self._version = redis_stats["redis_version"]
            self._uptime = str(datetime.timedelta(seconds = redis_stats["uptime_in_seconds"]))
        except:
            raise processmanager.ProcessManagerError("Could no retrive uptime")

    def connect(self):
        """
        Connect to the sql server
        """
        try:
            db = redis.StrictRedis(host=self._host, db=0)
        except all as e:
            raise processmanager.ProcessManagerError("Impossible to connect to the database serveur")
        else:
            #Create mysql object
            self._sql = db

    def kill(self, pid):
        """
        Kil a mysql threads
        """
        try:
            self._sql.execute('kill ' + pid)
        except MySQLdb.OperationalError as e:
            raise processmanager.ProcessManagerError("Impossible to kill pid : " + str(pid))
   

