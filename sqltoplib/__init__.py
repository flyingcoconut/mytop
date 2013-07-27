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

try: #Try to import MySQLdb library
    import MySQLdb
except ImportError:
    print "MySQL library is missing"

VERSION = "0.0.1"

class ProcessManagerError(Exception):
    """
    ProcessManager error class
    """
    def __init__(self, value):
        self.value = value
        Exception.__init__(self, value)
    def __str__(self):
        return repr(self.value)

class ConfigError(Exception):
    """
    Config error class
    """ 
    def __init__(self, value):
        self.value = value
        Exception.__init__(self, value)
    def __str__(self):
        return repr(self.value)

class Process(object):
    """
    A process class
    """
    def __init__(self, pid=0, user=None, host=None, db=None, state=None, time=0, info=None):
        self._pid = pid
        self._user = user
        self._host = host
        self._db = db
        self._state = state
        self._time = time
        self._info = info

    @property
    def pid(self):
        """
        Get process pid
        """
        return self._pid
    @pid.setter
    def pid(self, value):
        """
        Set process pid
        """
        self._pid = value

    @property
    def user(self):
        """
        Get user running process
        """
        return self._user
    @user.setter
    def user(self, value):
        """
        Set user running process
        """
        self._user = value

    @property
    def host(self):
        """
        Get host
        """
        return self._host
    @host.setter
    def host(self, value):
        """
        Set host
        """
        self._host = value

    @property
    def db(self):
        """
        Get database name
        """
        return self._db
    @db.setter
    def db(self, value):
        """
        Set database name
        """
        self._db = value

    @property
    def state(self):
        """
        Get process state
        """
        return self._state
    @state.setter
    def state(self, value):
        """
        Set process state
        """
        self._state = value

    @property
    def time(self):
        """
        Get process running time
        """
        return self._time
    @time.setter
    def time(self, value):
        """
        Set process running time
        """
        self._time = value

    @property
    def info(self):
        """
        Get info
        """
        return self._info
    @info.setter
    def info(self, value):
        """
        Set info
        """
        self._info = value


class ProcessManager(object):
    """
    A class to manipulate and get sql server process
    """
    MYSQL_BACKEND = "mysql"
    PGSQL_BACKEND = "pgsql"
    MONGODB = "mongodb"
    def __init__(self, backend=None, user="root", host="localhost", password=None, port=3306):
        self._backend = backend
        self._user = user
        self._host = host
        self._password = password
        self._port = port
        self._history = []
        self._max_history = 5
        self._version = "Unknown"
        self._uptime = 0
        self._process = []
        self._sql = None
        self._filter = {}
        
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
        if self._backend == "mysql":
            self._process_mysql()
            self._uptime_mysql()
            self._version_mysql()

    def history(self, pos):
        """
        Get proces based on history position
        """
        self._process = self._history[pos]

    def connect(self):
        """
        Connect to the sql server
        """
        if self._backend == "mysql":
            try:
                db = MySQLdb.connect(host=self._host, user=self._user, passwd=self._password, port=self._port)
            except MySQLdb.OperationalError as e:
                raise ProcessManagerError("Impossible to connect to the database serveur")
            else:
                #Create mysql object
                self._sql = db.cursor()

    def close(self):
        """
        Close sql server connection
        """
        self._sql.close()

    def kill(self, pid):
        """
        Kill a sql process/threads
        """
        if self._backend == "mysql":
            self._kill_mysql(pid)

    def _process_mysql(self):
        """
        Get a list of mysql threads
        """
        try:
            self._sql.execute('SHOW FULL PROCESSLIST;')
        except:
            raise ProcessManagerError("Could not retieve process")
        all_process = []
        try:
            for row in self._sql.fetchall():
                if len(str(row[5])) > 8 :
                    row[5] = "-"
                if row[3] is None:
                    db_name = "None"
                else:
                    db_name = row[3]
                if row[4].lower().strip() == 'query':
                    state = "Q"
                elif row[4].lower().strip() == 'sleep':
                    state = "S"
                elif row[4].lower().strip() == 'connect':
                    state = "C"
                elif row[4].lower().strip() == 'bindlog':
                    state = "B"
                else:
                    state = "U"
                if row[7] is None:
                    query = "None"
                else:
                    query = row[7]
                p = Process(row[0], row[1], row[2].split(':')[0], db_name, state, row[5], query)
                all_process.append(p)
        except:
            pass
        if len(self._history) > self._max_history:
            self._history.pop(0)
            self._history.append(self._process)
        else:
            self._history.append(self._process)
        self._process = all_process

    def _version_mysql(self):
        """
        Get mysql version
        """
        try:
            self._sql.execute('select VERSION();')
            self._version = self._sql.fetchone()[0]
        except:
            raise ProcessManagerError("Could no retrive version")

    def _uptime_mysql(self):
        """
        Get mysql uptime
        """
        try:
            self._sql.execute('show status where Variable_name="Uptime"')
            self._uptime = str(datetime.timedelta(seconds = int(self._sql.fetchone()[1])))
        except:
            raise ProcessManagerError("Could no retrive uptime")

    def _kill_mysql(self, pid):
        """
        Kil a mysql threads
        """
        try:
            self._sql.execute('kill ' + pid)
        except MySQLdb.OperationalError as e:
            raise ProcessManagerError("Impossible to kill pid : " + str(pid))
   
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

