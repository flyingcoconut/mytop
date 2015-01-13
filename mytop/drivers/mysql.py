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
"""MySQL Driver"""
import datetime

import driver
import MySQLdb

class MySQLDriver(driver.Driver):
    """MySQL Driver"""
    def __init__(self):
        driver.Driver.__init__(self)
        self.name = "mysql"
        self.config.add("host", default="localhost", required=False, validator=str)
        self.config.add("user", default="root", required=False, validator=str)
        self.config.add("port", default=3306, required=False, validator=int)
        self.config.add("password", default="", required=False, validator=str)
        self._sql = None

    def fields(self):
        """Return all disponible fields"""
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
        """Refresh sql list of running process"""
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
                if row[7] is None:
                    query = "None"
                else:
                    query = row[7].replace('\n', ' ')
                p = {}
                p["pid"] = row[0]
                p["user"] = row[1]
                p["host"] = row[2].split(':')[0]
                p["db"] = db_name
                p["state"] = row[4]
                p["time"] = row[5]
                p["info"] = query
                all_process.append(p)
        except all as e:
            raise driver.DriverError(e)
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
        """Initialize the driver"""
        try:
            db = MySQLdb.connect(host=self.config.host, user=self.config.user, passwd=self.config.password, port=self.config.port)
        except MySQLdb.OperationalError as e:
            raise driver.DriverError("Impossible to connect to the database serveur")
        else:
            #Create mysql object
            self._sql = db.cursor()

    def terminate(self):
        """Terminate connection"""
        self._sql.close()


    def kill(self, process):
        """Kill a mysql threads"""
        pass

    def explain(self, process):
        """Explain a mysql query"""
        pass
