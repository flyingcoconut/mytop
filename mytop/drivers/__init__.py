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
import importlib

__drivers__ = {
    'linux:process' : ['linux', 'LinuxProcessDriver'],
    'mysql' : ['mysql', 'MySQLDriver'],
    'redis' : ['redisdb', 'RedisDriver']
}

def list_drivers():
    return __drivers__.keys()

def load(driver):
    try:
        module_name = __drivers__[driver][0]
        driver_name = __drivers__[driver][1]
    except IndexError:
        print("ohoho")
    
    module = importlib.import_module("." + module_name, "sqltoplib.drivers")
    driver = getattr(module, driver_name)
    return driver()
