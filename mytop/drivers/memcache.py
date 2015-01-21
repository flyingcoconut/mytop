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
Memcache Driver
"""
import datetime
import time

import driver
import memcache


class MemcacheDriver(driver.Driver):
    """
    Memcache Driver
    """
    def __init__(self):
        driver.Driver.__init__(self)
        self._memcache = None

    def fields(self):
        """
        Return all disponible fields
        """
        fields = {}
        fields["pid"] = int
        fields["user"] = str
        fields["state"] = str
        fields["time"] = str
        fields["info"] = str
        return fields

    def tops(self):
        """
        Refresh sql information. Including uptime and the list of running process
        """
        all_process = []
        for pr in linux_process:
            info = pr.name + " " + " ".join(pr.cmdline)
            p = {}
            p["pid"] = int(pr.pid)
            p["user"] = str(pr.username)
            p["state"] = "s"
            p["time"] = int(pr.create_time)
            p["info"] = str(info)
            all_process.append(p)
        return all_process

    def info(self):
        pass

    def initialize(self):
        self._memcache = memcache.Client()


drivers = {"memcache" : MemcacheDriver}
