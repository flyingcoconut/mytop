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
Apache Driver
"""
import urllib2

from bs4 import BeautifulSoup
import urllib2
import driver


class ApacheDriver(driver.Driver):
    """
    Apache Driver
    """
    def __init__(self):
        driver.Driver.__init__(self)
        self.config.add("url", default="/status", required=False, validator=str)
        self.name = "apache"

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
        status_page = urllib2.urlopen(self.config.url)
        soup = BeautifulSoup(status_page.read())
        table = soup.table
        all_request = []
        for row in table.findAll("tr")[1:]:
            items = row.findAll("td")
            request = {}
            request["server"] = items[0].text
            request["pid"] = items[1].text
            request["access"] = items[2].text
            request["mode"] = items[3].text
            request["cpu"] = items[4].text
            request["seconds"] = items[5].text
            request["required"] = items[6].text
            request["connection"] = items[7].text
            request["child"] = items[8].text
            request["slot"] = items[9].text
            request["client"] = items[10].text
            request["vhost"] = items[11].text
            request["request"] = items[12].text
            all_request.append(request)
        return all_request

    def info(self):
        pass
