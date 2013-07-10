#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Patrick Charron
# Email : patrick.charron.pc@gmail.com
# Description : MySQL process viewer
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

try: #Try to import MySQLdb library
    import MySQLdb
except ImportError:
    print "MySQL library is missing"

VERSION = "0.0.1"

class processManagerError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class configError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class process(object):
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
        return self._pid
    @pid.setter
    def pid(self, value):
        self._pid = value

    @property
    def user(self):
        return self._user
    @user.setter
    def user(self, value):
        self._user = value

    @property
    def host(self):
        return self._host
    @host.setter
    def host(self, value):
        self._host = value

    @property
    def db(self):
        return self._db
    @db.setter
    def db(self, value):
        self._db = value

    @property
    def state(self):
        return self._state
    @state.setter
    def state(self, value):
        self._state = value

    @property
    def time(self):
        return self._time
    @time.setter
    def time(self, value):
        self._time = value

    @property
    def info(self):
        return self._info
    @info.setter
    def info(self, value):
        self._info = value


class processManager(object):
    MYSQL_BACKEND = "mysql"
    PGSQL_BACKEND = "pgsql"
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
        return self._user
    @user.setter
    def user(self, value):
        self._user = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def max_history(self):
        return self._max_history

    @max_history.setter
    def max_history(self, value):
        self._max_history = value

    @property
    def process(self):
        if len(self._filter) > 0:
            filtered_process = []
            for p in self._process:
                hits = 0
                for key in self._filter.keys():
                    if key == "pid":
                        try:
                            if re.match(self._filter[key], p.pid, flags=0):
                                hits = hits + 1
                        except:
                            pass
                    elif key == "user":
                        try:
                            if re.match(self._filter[key], p.user, flags=0):
                                hits = hits + 1
                        except:
                            pass
                    elif key == "host":
                        try:
                            if re.match(self._filter[key], p.host, flags=0):
                                hits = hits + 1
                        except:
                            pass
                    elif key == "db":
                        try:
                            if re.match(self._filter[key], p.db, flags=0):
                                hits = hits + 1
                        except:
                            pass
                    elif key == "state":
                        try:
                            if re.match(self._filter[key], p.state, flags=0):
                                hits = hits + 1
                        except:
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
        return self._version

    @property
    def uptime(self):
        return self._uptime

    def order_by(self, key, asc=True):
        print "todo"

    def add_filter(self, key, value):
        self._filter[key] = value

    def get_filter(self, key):
        try:
            return self._filter[key]
        except KeyError:
            return ""

    def del_filter(self, key):
        del self._filter[key]

    def del_all_filter(self):
        self._filter.clear()

    def list_filter(self):
        return self._filter.keys()

    def refresh(self):
        if self._backend == "mysql":
            self._process_mysql()
            self._uptime_mysql()
            self._version_mysql()

    def history(self, pos):
        self._process = self._history[pos]

    def connect(self):
        if self._backend == "mysql":
            try:
                db = MySQLdb.connect(host=self._host, user=self._user, passwd=self._password, port=self._port)
            except MySQLdb.OperationalError as e:
                raise processManagerError("Impossible to connect to the database serveur")
            else:
                #Create mysql object
                self._sql = db.cursor()

    def close(self):
        self._sql.close()

    def kill(self, pid):
        if self._backend == "mysql":
            self._kill_mysql(pid)

    def _process_mysql(self):
        try:
            self._sql.execute('SHOW FULL PROCESSLIST;')
        except:
            raise processManagerError("Could not retieve process")
        all_process = []
        try:
            for row in self._sql.fetchall():
                if len(str(row[5])) > 8 :
                    row[5] = "-"
                if row[3] is None:
                    dbName = "None"
                else:
                    dbName = row[3]
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
                p = process(row[0], row[1], row[2].split(':')[0], dbName, state, row[5], query)
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
        try:
            self._sql.execute('select VERSION();')
            self._version = self._sql.fetchone()[0]
        except:
            raise processManagerError("Could no retrive version")

    def _uptime_mysql(self):
        try:
            self._sql.execute('show status where Variable_name="Uptime"')
            self._uptime = str(datetime.timedelta(seconds = int(self._sql.fetchone()[1])))
        except:
            raise processManagerError("Could no retrive uptime")

    def _kill_mysql(self, pid):
        try:
            self._sql.execute('kill ' + pid)
        except MySQLdb.OperationalError as e:
            raise processManagerError("Impossible to kill pid : " + str(pid))
            


class processAgregator(object):
    def __init__(self):
        self._db = []

    def remove(self, db):
        print "todo"

    def append(self, db):
        self._db.append(db)
    
    def connect(self):
        for db in self._db:
            db.connect()

    def refresh(self):
        for db in self._db:
            db.refresh()

    def close(self):
        for db in self._db:
            db.close()

    def kill(self, process):
        print "todo"

    @property
    def process(self):
        tmp_process = []
        for db in self._db:
            for p in db.process:
                tmp_process.append(p)
        return tmp_process

class config(object):
    """
    A class to read and write config
    """
    def __init__(self, path = None):
        self._path = path
        self._options = {}
        self._comments = {}

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    def get_option(self, option):
        try:
            return self._options[option]
        except KeyError:
            return None

    def set_option(self, option, value):
        self._options[option] = value

    def write(self):
        print "todo"

    def parse(self):
        self._options = {}
        f = open(self._path)
        for l in f.readlines():
            line = l.strip()
            if line[0] == "#":
                pass
            else:
                line = line.split("=")
                self._options[line[0].strip()] = line[1].strip()
        f.close()

