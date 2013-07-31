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
