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

class processManager():
    MYSQL_BACKEND = "mysql"
    PGSQL_BACKEND = "pgsql"
    def __init__(self, backend, db):
        self.backend = backend
        self.max_history
        self.history = []
        self.max_history = 5
        self.info["version"] = "Unknown"
        self.info["user"] = "Unknow"
        self.info["uptime"] = 0
        if backend == "mysql":
            self.sql = db.cursor()
        
    def get_process(self):
        if self.backend == "mysql":
            self._process_mysql()
            return self.process
    def get_info():
        if self.backend == "mysql":
            self._info_mysql()
            return self.info
    def kill(self, pid):
        if self.backend == "mysql":
            self._kill_mysql(self, pid)
    def _process_mysql(self):
        self.sql.execute('SHOW FULL PROCESSLIST;')
        try:
            for row in sql.fetchall():
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
                self.process = []
                self.process.append(p)
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

class processCluster():
    def __init__(self):
        print "todo"

