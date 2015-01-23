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

import driver

class pgSQLDriver(driver.Driver):
    """
    A class to manipulate and get sql server process
    """
    def __init__(self, user="root", host="localhost", password=None, port=3306):
        pass

    def tops(self):
        """
        Refresh sql information. Including uptime and the list of running process
        """
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
        except all as error:
            raise driver.DriverError(error)
        return all_process
