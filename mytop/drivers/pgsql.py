#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Patrick Charron
# Email : patrick.charron.pc@gmail.com
# Description : Top Informations Viewer
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

import datetime
import re

import driver

class pgSQLDriver(driver.Driver):
    """
    A class to manipulate and get sql server process
    """
    def __init__(self, user="root", host="localhost", password=None, port=3306):
        processmanager.ProcessManager.__init__(self, user, host, password, port)

    def refresh(self):
        """
        Refresh sql information. Including uptime and the list of running process
        """
        try:
            mongodb_process = self._sql.admin['$cmd.sys.inprog'].find_one({'$all': True})
        except:
            raise processmanager.ProcessManagerError("Could not retieve process")
        all_process = []
        try:
            for row in mongodb_process[u"inprog"]:
                if row[u"active"]:
                    time = row[u"secs_running"]
                else:
                    time = 0
                if row[u"op"] == "insert":
                    state = "I"
                elif row[u"op"] == "query":
                    state = "Q"
                elif row[u"op"] == "update":
                    state = "U"
                elif row[u"op"] == "remove":
                    state = "R"
                elif row[u"op"] == "getmore":
                    state = "G"
                elif row[u"op"] == "command":
                    state = "C"
                p = process.Process(row["opid"], "", row[u"client"].split(':')[0], row[u"ns"].split(".")[0], state, time, str(row[u"query"]))
                all_process.append(p)
        except all as e:
            print(e)
            pass
        if len(self._history) > self._max_history:
            self._history.pop(0)
            self._history.append(self._process)
        else:
            self._history.append(self._process)
        self._process = all_process
        #try:
        #    self._sql.execute('show status where Variable_name="Uptime"')
        #    self._uptime = str(datetime.timedelta(seconds = int(self._sql.fetchone()[1])))
        #except MySQLdb.OperationalError:
        #    raise processmanager.ProcessManagerError("Could no retrive uptime")
        #try:
        #    self._sql.execute('select VERSION();')
        #    self._version = self._sql.fetchone()[0]
        #except:
        #    raise processmanager.ProcessManagerError("Could no retrive version")

    def connect(self):
        """
        Connect to the sql server
        """
        db = pymongo.MongoClient(host=self._host, port=self._port)
#        except MySQLdb.OperationalError as e:
#            raise processmanager.ProcessManagerError("Impossible to connect to the database serveur")
#        else:
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
