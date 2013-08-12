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
sqloptlib is a library to manipulate and get sql server process
"""

import getopt
import datetime
import re
import pwd
import os

DISPONIBLE_BACKEND = []
try:
    import mysql
    DISPONIBLE_BACKEND.append("mysql")
except all as e:
    pass

try:
    import mongodb
    DISPONIBLE_BACKEND.append("mongodb")
except all as e:
    print e
    pass

try:
    import redisdb
    DISPONIBLE_BACKEND.append("redisdb")
except all as e:
    pass

try:
    import pgsql
    DIPONIBLE_BACKEND.append("pgsql")
except:
    pass

try:
    import linux
    DISPONIBLE_BACKEND.append("linux")
except all as e:
    pass
    
try:
    import dummy
except all as e:
    pass


class ConfigError(Exception):
    """
    Config error class
    """ 
    def __init__(self, value):
        self.value = value
        Exception.__init__(self, value)
    def __str__(self):
        return repr(self.value)

class Config(object):
    """
    A class to read and write config
    """

    def __init__(self, path = None):
        self._path = path
        self._configs = {}
        self._comments = {}

    @property
    def path(self):
        """
        Get config path
        """
        return self._path

    @path.setter
    def path(self, value):
        """
        Set config path
        """
        self._path = value

    def get_config(self, config):
        """
        Get a config value
        """
        try:
            return self._configs[config]
        except KeyError:
            return None

    def set_config(self, config, value):
        """
        Set a config value
        """
        self._configs[config] = value

    def write(self):
        """
        Write config to file
        """
        print "todo"

    def parse(self):
        """
        Parse the configuration file
        """
        self._configs = {}
        config_file = open(self._path)
        for line in config_file.readlines():
            line = line.strip()
            if line[0] == "#":
                pass
            else:
                line = line.split("=")
                self._configs[line[0].strip()] = line[1].strip()
        config_file.close()

def create_connection(backend=None, user=None, host="localhost", password=None, port=None):
    if backend == "mysql":
        if user is None:
            user = "root"
        elif host is None:
            host = "localhost"
        elif password is None:
            password = ""
        elif port is None:
            port = 3306
        conn = mysql.ProcessManager(user, host, password, port)
        return conn
    elif backend == "mongodb":
        conn = mongodb.ProcessManager(user, host, password, port)
        return conn
    elif backend == "linux":
        user = pwd.getpwuid(os.getuid())[0]
        host = "localhost"
        port = "None"
        conn = linux.ProcessManager(user, host, password, port)
        return conn
    elif backend == "dummy":
        conn = dummy.ProcessManager()
        return conn

