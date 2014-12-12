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
MySQL Driver
"""
import datetime
import re

import driver
import MySQLdb

class MySQLDriver(driver.Driver):
    """
    MySQL Driver
    """
    def __init__(self):
        driver.Driver.__init__(self)
        self.config.add("host", default="localhost", required=False, validator=str)
        self.config.add("user", default="root", required=False, validator=str)
        self.config.add("port", default=3306, required=False, validator=int)
        self.config.add("password", default="", required=False, validator=str)
        self._sql = None

    def fields(self):
        """
        Return all disponible fields
        """
        fields = {}
        fields["pid"] = int
        fields["user"] = str
        fields["host"] = str
        fields["db"] = str
        fields["state"] = str
        fields["time"] = str
        fields["info"] = str
        return fields
        
    def tops(self):
        """
        Refresh sql information. Including uptime and the list of running process
        """
        try:
            self._sql.execute('SHOW FULL PROCESSLIST;')
        except:
            raise driver.DriverError("Could not retrieve process")
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
            raise DriverError(e)
        return all_process

    def info(self):
        try:
            self._sql.execute('show status where Variable_name="Uptime"')
            self._uptime = str(datetime.timedelta(seconds = int(self._sql.fetchone()[1])))
        except MySQLdb.OperationalError:
            raise driver.DriverError("Could no retrive uptime")
        try:
            self._sql.execute('select VERSION();')
            self._version = self._sql.fetchone()[0]
        except:
            raise driver.DriverError("Could no retrive version")

    def initialize(self):
        """
        Initialize the driver
        """
        try:
            db = MySQLdb.connect(host=self.config.host, user=self.config.user, passwd=self.config.password, port=self.config.port)
        except MySQLdb.OperationalError as e:
            raise driver.DriverError("Impossible to connect to the database serveur")
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

drivers = {"mysql": MySQLDriver}
