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

import getopt
import datetime
import re

import processmanager
import process

class ProcessManagerError(Exception):
    """
    ProcessManager error class
    """
    def __init__(self, value):
        self.value = value
        Exception.__init__(self, value)
    def __str__(self):
        return repr(self.value)

class ProcessManager(object):
    """
    A base class to manipulate and get sql server process
    """
    def __init__(self, user="root", host="localhost", password=None, port=None):
        self._user = user
        self._host = host
        self._password = password
        self._port = port
        self._history = []
        self._max_history = 5
        self._version = "Unknown"
        self._uptime = 0
        self._process = []
        self._filter = {}
        self._is_online = False
        self._error = None
        
    @property
    def user(self):
        """
        Get user
        """
        return self._user
    @user.setter
    def user(self, value):
        """
        Set user
        """
        self._user = value

    @property
    def password(self):
        """
        Get password
        """
        return self._password

    @password.setter
    def password(self, value):
        """
        Set password
        """
        self._password = value

    @property
    def host(self):
        """
        Get hostname
        """
        return self._host

    @host.setter
    def host(self, value):
        """
        Set hostname
        """
        self._host = value

    @property
    def port(self):
        """
        Get port number
        """
        return self._port

    @port.setter
    def port(self, value):
        """
        Set port number
        """
        self._port = value

    @property
    def max_history(self):
        """
        Get max history buffer
        """
        return self._max_history

    @max_history.setter
    def max_history(self, value):
        """
        Set max history buffer
        """
        self._max_history = value

    @property
    def process(self):
        """
        Get process
        """
        if len(self._filter) > 0:
            filtered_process = []
            for p in self._process:
                hits = 0
                for key in self._filter.keys():
                    if key == "pid":
                        try:
                            if re.match(self._filter[key], p.pid, flags=0):
                                hits = hits + 1
                        except re.error:
                            pass
                    elif key == "user":
                        try:
                            if re.match(self._filter[key], p.user, flags=0):
                                hits = hits + 1
                        except re.error:
                            pass
                    elif key == "host":
                        try:
                            if re.match(self._filter[key], p.host, flags=0):
                                hits = hits + 1
                        except re.error:
                            pass
                    elif key == "db":
                        try:
                            if re.match(self._filter[key], p.db, flags=0):
                                hits = hits + 1
                        except re.error:
                            pass
                    elif key == "state":
                        try:
                            if re.match(self._filter[key], p.state, flags=0):
                                hits = hits + 1
                        except re.error:
                            pass
                    elif key == "time":
                        if re.match(self._filter[key], p.time, flags=0):
                            hits = hits + 1
                    elif key == "info":
                        if re.match(self._filter[key], p.info, flags=0):
                            hits = hits + 1
                    if hits == len(self._filter.keys()):
                        filtered_process.append(p)
            return filtered_process
        else:
            return self._process

    @property
    def version(self):
        """
        Get sql server version
        """
        return self._version

    @property
    def is_online(self):
        """
        Get status
        """
        return self._is_online
    
    @property
    def error(self):
        """
        Get status
        """
        return self._error
    
    @property
    def uptime(self):
        """
        Get sql server uptime
        """
        return self._uptime

    def order_by(self, key, asc=True):
        """
        Order process by key
        """
        print "todo"

    def add_filter(self, key, value):
        """
        Add a filter
        """
        self._filter[key] = value

    def get_filter(self, key):
        """
        Get a filter value
        """
        try:
            return self._filter[key]
        except KeyError:
            return ""

    def del_filter(self, key):
        """
        Delete a filter
        """
        del self._filter[key]

    def del_all_filter(self):
        """
        Delete all filter
        """
        self._filter.clear()

    def list_filter(self):
        """
        List all filter. Return a dict
        """
        return self._filter.keys()

    def refresh(self):
        """
        Refresh sql information. Including uptime and the list of running process
        """
        pass

    def history(self, pos):
        """
        Get proces based on history position
        """
        self._process = self._history[pos]

    def connect(self):
        """
        Connect to the sql server
        """
        self._sql = db.cursor()

    def disconnect(self):
        self._sql = None
        self._is_online = False
        self._process = []

    def close(self):
        """
        Close sql server connection
        """
        self._sql.close()
