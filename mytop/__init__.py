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

import MySQLdb

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
        if self._backend == "mysql":
            return self._process

    @property
    def version(self):
        if self._backend == "mysql":
            self._version_mysql()
            return self._version

    @property
    def uptime(self):
        if self._backend == "mysql":
            self._uptime_mysql()
            return self._uptime
    
    def refresh(self):
        if self._backend == "mysql":
            self._process_mysql()

    def connect(self):
        if self._backend == "mysql":
            try:
                db = MySQLdb.connect(host=self._host, user=self._user, passwd=self._password, port=self._port)
            except MySQLdb.OperationalError as e:
                print e[1]
            else:
                #Create mysql object
                self._sql = db.cursor()

    def close(self):
        self._sql.close()
        self._sql = None

    def kill(self, pid):
        if self._backend == "mysql":
            self._kill_mysql(self, pid)

    def _process_mysql(self):
        self._sql.execute('SHOW FULL PROCESSLIST;')
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
            self._process = all_process
            self._history.append(p)
        except:
            pass

    def _version_mysql(self):
        self._sql.execute('select VERSION();')
        self._version = self._sql.fetchone()[0]

    def _uptime_mysql(self):
        self._sql.execute('show status where Variable_name="Uptime"')
        self._uptime = str(datetime.timedelta(seconds = int(self._sql.fetchone()[1])))

    def _kill_mysql(self, pid):
        self._sql.execute('kill ' + pid)

class processAgregator(object):
    def __init__(self):
        self._db = []


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
    A class to read and write mytop config
    """
    def __init__(self, path):
        self.path = path

    def write(self):
        print "todo"

    def parse(self):
        f = open(self.path)
        for l in f.readlines():
            print l

class argsParser(object):
    """
    A class to pass command line arguments
    """
    def __init__(self):
        print "todo"
        self.host = "localhost"
        self.password = None
        self.port = 3306
        self.user = "root"

    def parse(self, args):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h:p:P:u:V", ["host=", "password=", "port=", "user=", "version", "help"])
        except getopt.GetoptError, err:
            # print help information and exit:
            show_usage()
            print str(err) # will print something like "option -a not recognized"
            sys.exit(1)
        for o, a in opts:
            if o in ("-h", "--host"):
                options["host"] = a
            elif o in ("-p", "--password"):
                options["password"] = a
            elif o in ("-P", "--port"):
                options["port"] = int(a)
            elif o in ("-u", "--user"):
                options["user"] = a
            elif o in ("-V", "--version"):
                print "Version %s" % VERSION
                sys.exit(0)
            elif o == "--help":
                show_usage()
                show_help()
                sys.exit(0)
            else:
                show_usage()
                sys.exit(1)

        if options["password"] is None:
            options["password"] = getpass.getpass()