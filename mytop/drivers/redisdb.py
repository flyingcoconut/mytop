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
"""Redis Driver"""
import datetime

from .. import driver
import redis

class RedisDriver(driver.Driver):
    """
    Redis Driver
    """
    def __init__(self):
        driver.Driver.__init__(self)
        self.config.add("host", default="localhost", required=False, validator=str)
        self._sql = None
        
    def tops(self):
        """
        Refresh redis informations
        """
        try:
            redis_process = self._sql.client_list()
        except Exception as e:
            raise driver.DriverError("Could not retieve process : " + str(e))
        all_process = []
        try:
            for row in redis_process:
                p = {}
                p["address"] = row["addr"].split(':')[0]
                p["db"] = row["db"]
                p["flags"] = row["flags"]
                p["cmd"] = row["cmd"]
                all_process.append(p)
        except all as e:
            print e
            pass
        return all_process

    def info(self):
        try:
            redis_stats = self._sql.info()
            self._version = redis_stats["redis_version"]
            self._uptime = str(datetime.timedelta(seconds = redis_stats["uptime_in_seconds"]))
        except:
            raise driver.DriverError("Could no retrive uptime")

    def initialize(self):
        """
        Initialize redis connection
        """
        try:
            db = redis.StrictRedis(host=self.config.host, db=0)
        except Exception as e:
            raise driver.DriverError("Impossible to connect to the database serveur : " + str(e))
        self._sql = db
   

