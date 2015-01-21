#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Patrick Charron
# Email : patrick.charron.pc@gmail.com
# Description : Top Informations Viewer
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
    'linux:network' : ['linux', 'LinuxNetworkDriver'],
    'linux:disk' : ['linux', 'LinuxDiskDriver'],
    'linux:socket' : ['linux', 'LinuxSocketDriver'],
    'linux:cpu' : ['linux', 'LinuxCpuDriver'],
    'mysql' : ['mysql', 'MySQLDriver'],
    'redis' : ['redisdb', 'RedisDriver'],
    'apache': ['apache', 'ApacheDriver'],
    'elasticsearch' : ['elasticsearch', 'ElasticsearchDriver'],
}

def list_drivers():
    return __drivers__.keys()

def load(driver):
    try:
        module_name = __drivers__[driver][0]
        driver_name = __drivers__[driver][1]
    except KeyError:
        raise ValueError("Driver : " + str(driver) + " : is not valid")

    try:
        module = importlib.import_module("." + module_name, "mytop.drivers")
        driver = getattr(module, driver_name)
    except Exception as e:
        raise ImportError("Impossible to load : " + str(driver) + " : " + str(e))
    return driver()
