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
Plugin Driver

Load an external driver
Usefull for non official driver
"""
import driver

class PluginDriver(driver.Driver):
    """
    Plugin Driver
    """
    def __init__(self):
        driver.Driver.__init__(self)
        self.config.add("path", default=None, required=True, validator=None)
        self.config.add("config", default={}, required=False, validator=dict)
        
    def initialize(self):
        #Do some magic
        pass
   
