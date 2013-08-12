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
import platform
import time

import processmanager
import process

class ProcessManager(processmanager.ProcessManager):
    """
    A class to manipulate and get sql server process
    """
    def __init__(self):
        processmanager.ProcessManager.__init__(self, user="Unknown", host="Unknown", password="", port=0)
        self.BACKEND = "Unknown"
        
        
        
    def refresh(self):
        """
        Refresh sql information. Including uptime and the list of running process
        """
        self._process = []
        self._uptime = "Unknown"
        self._version = "Unknown"

    def connect(self):
        pass
   
