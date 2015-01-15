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
        self._timeline = {}

    def add(self, items):
        """Add a frame"""
        self._items.append(items)
        self._timeline[time.time()] = items

    def last(self):
        """Return last frame"""
        try:
            items = self._items[-1]
        except IndexError:
            items = []
        return items

    def first(self):
        """Return first frame"""
        pass

    def __len__(self):
        return len(self._items)

class Session(threading.Thread):
    STATUS_STOPPED = 0
    STATUS_INITIALIZING = 1
    STATUS_RUNNING = 2
    STATUS_PAUSED = 3
    STATUS_ERROR = 4
    def __init__(self, driver, config, history=10):
        threading.Thread.__init__(self)
        self.daemon = True
        self.driver = driver
        self.config = config
        self.filters = []
        self.history = History(history)
        self.delay = 1
        self.status = self.STATUS_STOPPED
        self.last_error = None

    def run(self):
        """Start the session"""
        self.status = self.STATUS_INITIALIZING
        try:
            self.driver.configure(self.config)
            self.driver.initialize()
        except Exception as error:
            self.status = self.STATUS_ERROR
            self.last_error = error.value
        self.status = self.STATUS_RUNNING
        while (self.status == self.STATUS_RUNNING):
            try:
                items = self.driver.tops()
                self.history.add(items)
            except Exception as error:
                self.status = self.STATUS_ERROR
                self.last_error = error.value
            time.sleep(self.delay)

    def stop(self):
        """Stop the session"""
        self.status = self.STATUS_STOPPED
        self.driver.terminate()

    def pause(self):
        """Pause the session"""
        self.status = self.STATUS_PAUSED

    def resume(self):
        """Resume the session"""
        pass

    def record(self):
        """Record a session"""
        pass

    def tops(self):
        items = self.driver.tops()
        #self.history.add(items)
        return items

    def fields(self):
        return self.driver.fields()

    def info(self):
        return self.driver.info()

    def additional(self):
        pass


# class SessionsManager(object):
#     """Sessions Manager"""
#     def __init__(self):
#         self.current = None
#         self.sessions = []
#         self.next_uid = 0
#
#     def remove(self):
#         """Remove a session"""
#         pass
#
#     def print_data(self, tops):
#         print(tops)
#
#     def new(self, driver, config):
#         """Create a new session"""
#         session = Session(self.next_uid, driver, config)
#         session.callback = self.print_data
#         self.next_uid = self.next_uid + 1
#         self.sessions.append(session)
#         session.start()
#
#     def enable(self):
#         pass
#
#     def disable(self):
#         pass



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
                    "length": 40,
                    "alignment": "left",
                    "title": "Info"
                },
                "pid": {
                    "position": 0,
                    "length": 10,
                    "alignment": "right",
                    "title": "Pid"
                },
                "db": {
                    "position": 3,
                    "length": 20,
                    "alignment": "left",
                    "title": "Database"
                },
                "state": {
                    "position": 4,
                    "length": 7,
                    "alignment": "left",
                    "title": "State"
                },
                "host": {
                    "position": 2,
                    "length": 15,
                    "alignment": "left",
                    "title": "Hostname"
                },
                "user": {
                    "position": 1,
                    "length": 11,
                    "alignment": "left",
                    "title": "Username"
                },
                "time": {
                    "position": 5,
                    "length": 8,
                    "alignment": "left",
                    "title": "Uptime"
                }
            },
            "headers": {}
        },
        "linux:process": {
            "process": {
                "pid": {
                    "position": 0,
                    "length": 5,
                    "alignment": "right",
                    "title": "PID"
                },
                "user": {
                    "position": 1,
                    "length": 9,
                    "alignment": "left",
                    "title": "USER"
                },
                "nice": {
                    "position": 2,
                    "length": 2,
                    "alignment": "right",
                    "title": "NI"
                },
                "vms": {
                    "position": 3,
                    "length": 7,
                    "alignment": "right",
                    "title": "VIRT"
                },
                "rss": {
                    "position": 4,
                    "length": 6,
                    "alignment": "right",
                    "title": "RES"
                },
                "shared": {
                    "position": 5,
                    "length": 6,
                    "alignment": "right",
                    "title": "SHR"
                },
                "state": {
                    "position": 6,
                    "length": 1,
                    "alignment": "right",
                    "title": "S"
                },
                "cpu": {
                    "position": 7,
                    "length": 4,
                    "alignment": "right",
                    "title": "%CPU"
                },
                "memory": {
                    "position": 8,
                    "length": 4,
                    "alignment": "right",
                    "title": "%MEM"
                },
                "time": {
                    "position": 9,
                    "length": 8,
                    "alignment": "right",
                    "title": "TIME+"
                },
                "command": {
                    "position": 10,
                    "length": 10,
                    "alignment": "left",
                    "title": "COMMAND"
                }
            },
            "headers": {}
        }
    }
}
