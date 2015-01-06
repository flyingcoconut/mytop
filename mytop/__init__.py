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

import datetime
import os
import time
import threading

class History(object):
    def __init__(self, lenght=0):
        self.lenght = lenght
        self._items = []

    def add(self, items):
        self._items[time.time()] = items

    def get(self):
        pass

class Session(threading.Thread):
    def __init__(self, driver, config, history=10):
        threading.Thread.__init__(self)
        self.driver = driver
        self.config = config
        self.filters = []
        self.history = History(history)
        self.interval = 1

    def start(self):
        """Start the session"""
        self.driver.configure(self.config)
        self.driver.initialize()

    def stop(self):
        """Stop the session"""
        self.driver.terminate()

    def pause(self):
        """Pause the session"""
        pass

    def resume(self):
        """Resume the session"""
        pass

    def record(self):
        """Record a session"""
        pass

    def tops(self):
        items = self._driver.tops()
        #self.history.add(items)
        return items

    def fields(self):
        return self._driver.fields()

    def info(self):
        return self._driver.info()

    def additional(self):
        pass


class SessionsManager(object):
    """Sessions Manager"""
    def __init__(self):
        self.current = None
        self.sessions = []

    def remove(self):
        """Remove a session"""
        pass

    def add(self, session):
        """Create a new session"""
        self.sessions.append(session)

    def enable(self):
        pass

    def disable(self):
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


default_config = {
    "drivers": {
        "mysql": {
            "process": {
                "info": {
                    "position": 6,
                    "length": 5,
                    "aligment": "left",
                    "title": "Info"
                },
                "pid": {
                    "position": 0,
                    "length": 10,
                    "aligment": "right",
                    "title": "Pid"
                },
                "db": {
                    "position": 3,
                    "length": 20,
                    "aligment": "left",
                    "title": "Database"
                },
                "state": {
                    "position": 4,
                    "length": 5,
                    "aligment": "left",
                    "title": "State"
                },
                "host": {
                    "position": 2,
                    "length": 15,
                    "aligment": "left",
                    "title": "Hostname"
                },
                "user": {
                    "position": 1,
                    "length": 11,
                    "aligment": "left",
                    "title": "Username"
                },
                "time": {
                    "position": 5,
                    "length": 8,
                    "aligment": "left",
                    "title": "Uptime"
                }
            },
            "headers": {}
        }
    }
}
