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
"""
MongoDB Driver
"""
import datetime

import driver
import pymongo

class MongoDBDriver(driver.Driver):
    """
    MongoDB Driver class
    """
    def __init__(self):
        driver.Driver.__init__(self)
        self._host = None
        self._port = None

    def tops(self):
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

        mongodb_stats = self._sql.admin.command('serverStatus', 1)
        self._uptime = str(datetime.timedelta(seconds = mongodb_stats["uptime"]))
        self._version = mongodb_stats["version"]

    def initialize(self):
        """Connect to the MongoDB server"""
        try:
            db = pymongo.MongoClient(host=self._host, port=self._port)
        except MySQLdb.OperationalError as e:
            raise driver.DriverError("Impossible to connect to the database serveur")
        self._sql = db

    def configure(self, conf):
        self.config = conf
        try:
            self._host = self.config["host"]
            self._port = self.config["port"]
        except:
            raise driver.DriverError("Bad config")
