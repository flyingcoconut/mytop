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
sqltoplib MySQL backend
"""

import datetime
import re

import processmanager

try: #Try to import MySQLdb library
    import MySQLdb
except ImportError:
     raise processmanager.ProcessManagerError("mysql backend not disponible")
     
try:
    import sqlparse
except ImportError:
    pass

class ProcessManager(processmanager.ProcessManager):
    """
    A class to manipulate and get sql server process
    """
    def __init__(self, user, host, password, port):
        processmanager.ProcessManager.__init__(self, user, host, password, port)
        self.BACKEND = "mysql"
        
    def refresh(self):
        """
        Refresh sql information. Including uptime and the list of running process
        """
        try:
            self._sql.execute('SHOW FULL PROCESSLIST;')
        except:
            self._is_online = False
            self._error = "Could not retrieve process"
            raise processmanager.ProcessManagerError("Could not retrieve process")
        all_process = []
        try:
            for row in self._sql.fetchall():
                if len(str(row[5])) > 8 :
                    row[5] = "-"
                if row[3] is None:
                    db_name = "None"
                else:
                    db_name = row[3]
                if row[4].lower().strip() == 'query':
                    state = "Q"
                elif row[4].lower().strip() == 'sleep':
                    state = "S"
                elif row[4].lower().strip() == 'connect':
                    state = "C"
                elif row[4].lower().strip() == 'bindlog':
                    state = "B"
                else:
                    state = "U"
                if row[7] is None:
                    query = "None"
                else:
                    query = row[7]
                p = {}
                p["pid"] = row[0]
                p["user"] = row[1]
                p["host"] = row[2].split(':')[0]
                p["db"] = db_name
                p["state"] = state
                p["time"] = row[5]
                p["info"] = query
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
            self._sql.execute('show status where Variable_name="Uptime"')
            self._uptime = str(datetime.timedelta(seconds = int(self._sql.fetchone()[1])))
        except MySQLdb.OperationalError:
            raise processmanager.ProcessManagerError("Could no retrive uptime")
        try:
            self._sql.execute('select VERSION();')
            self._version = self._sql.fetchone()[0]
        except:
            raise processmanager.ProcessManagerError("Could no retrive version")

    def connect(self):
        """
        Connect to the sql server
        """
        try:
            db = MySQLdb.connect(host=self._host, user=self._user, passwd=self._password, port=self._port)
        except MySQLdb.OperationalError as e:
            self._is_online = False
            self._error = "Impossible to connect to the database serveur"
            raise processmanager.ProcessManagerError("Impossible to connect to the database serveur")
        else:
            #Create mysql object
            self._sql = db.cursor()
            self._is_online = True

    def kill(self, process):
        """
        Kil a mysql threads
        """
        try:
            self._sql.execute('kill ' + process.pid)
        except MySQLdb.OperationalError as e:
            raise processmanager.ProcessManagerError("Impossible to kill pid : " + str(pid))
    
    def explain(self, process):
        """
        Explain a mysql query
        """
        print "todo"
   

