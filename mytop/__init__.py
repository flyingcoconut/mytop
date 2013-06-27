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

import MySQLdb

class processManager(object):
    MYSQL_BACKEND = "mysql"
    PGSQL_BACKEND = "pgsql"
    def __init__(self, backend, user="root", host="localhost", password=None, port=3306):
        self.backend = backend
        self.user = user
        self.host = host
        self.password = password
        self.port = port
        self.history = []
        self.max_history = 5
        self.version = "Unknown"
        self._uptime = 0
        self._process = []
        if backend == "mysql":
            try:
                db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, port=self.port)
            except MySQLdb.OperationalError as e:
                print e[1]
            else:
                #Create mysql object
                self.sql = db.cursor()

    @property
    def process(self):
        if self.backend == "mysql":
            self._process_mysql()
            return self._process

    @property
    def uptime(self):
        return 
        
    def get_process(self):
        if self.backend == "mysql":
            self._process_mysql()
            return self.process

    def get_info(self):
        if self.backend == "mysql":
            self._info_mysql()
            return self.info

    def kill(self, pid):
        if self.backend == "mysql":
            self._kill_mysql(self, pid)

    def _process_mysql(self):
        self.sql.execute('SHOW FULL PROCESSLIST;')
        process = []
        try:
            for row in self.sql.fetchall():
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
                p = [row[0], row[1], row[2].split(':')[0], dbName, state, row[5], query]
                process.append(p)
            self._process = process
            self.history.append(p)
        except:
            pass

    def _info_mysql(self):
        self.sql.execute('select VERSION();')
        self.info["version"] = sql.fetchone()[0]
        self.info["user"] = user
        self.sql.execute('show status where Variable_name="Uptime"')
        self.info["uptime"] = str(datetime.timedelta(seconds = int(sql.fetchone()[1])))
    def _kill_mysql(self, pid):
        self.sql.execute('kill ' + pid)
        #except MySQLdb.OperationalError as e:

class processAgregator(object):
    def __init__(self):
        print "todo"

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