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
Elasticsearch Drivers
"""
import urllib2
import json

from . import driver


class ElasticsearchDriver(driver.Driver):
    """
    Apache Driver
    """
    def __init__(self):
        driver.Driver.__init__(self)
        self.config.add("url", default="http://localhost/status", required=False, validator=str)
        self.name = "elasticsearch"

    def fields(self):
        pass

    def tops(self):
        """
        Refresh sql information. Including uptime and the list of running process
        """
        status_page = urllib2.urlopen(self.config.url)
        stats = json.loads(status_page.read())
        all_indices = []
        for key in stats["indices"].keys():
            informations = stats["indices"][key]
            index = {}
            index["index"] = key
            index["size"] = informations["index"]["size_in_bytes"]
            index["max_doc"] = informations["docs"]["max_doc"]
            index["num_doc"] = informations["docs"]["num_docs"]
            index["deleted_doc"] = informations["docs"]["deleted_docs"]
            index["merges_total_docs"] = informations["merges"]["total_docs"]
            index["merges_total_size"] = informations["merges"]["total_size_in_bytes"]
            index["merges_current_docs"] = informations["merges"]["current_docs"]
            index["merges_current"] = informations["merges"]["current"]
            index["merges_total_time"] = informations["merges"]["total_time_in_millis"]
            index["merges_total"] = informations["merges"]["total"]
            index["shards"] = len(informations["shards"].keys())
            index["refresh_total_time"] = informations["refresh"]["total_time_in_millis"]
            index["refresh_total"] = informations["refresh"]["total"]
            index["flush_total_time"] = informations["flush"]["total_time_in_millis"]
            index["flush_total"] = informations["flush"]["total"]
            all_indices.append(index)
        return all_indices

    def info(self):
        pass
