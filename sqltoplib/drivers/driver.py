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
Base Class Driver
"""

class DriverError(Exception):
    """
    Driver error class
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class DriverConfig(object):
    """
    Driver config class
    """
    def __init__(self):
        self._configs = {}

    def add(self, name, default=None, required=True, validator=None):
        self._configs[name] = {}
        self._configs[name] = [default, required, validator]

    def parse(self, config):
        """
        Parse config
        """
        for key in self._configs.keys():
            if key in config:
                if self._configs[key][2]:
                    #Validate
                    try:
                       value = self._configs[key][2](config[key])
                    except:
                       raise DriverError("Impossible to validate")
                    else:
                       setattr(self, key, value)
                else:
                    setattr(self, key, value)
            else:
                if self._configs[key][1]:
                    #Verify if required
                    raise DriverError("Configuration key : " + key + " is required")
                else:
                    setattr(self, key, self._configs[key][0])

class Driver(object):
    """
    Base class Driver
    """
    def __init__(self):
        self.config = DriverConfig()
     
    def tops(self):
        """
        Refresh informations.
        """
        return {}

    def fields(self):
        """
        Return fields description
        """
        return {}

    def info(self):
        """
        Return info about driver
        """
        return {}

    def initialize(self):
        """
        Initialize the driver
        """
        pass

    def terminate(self):
        """
        Terminate driver
        """
        pass

    def configure(self, config):
        """
        Configure driver parameter
        """
        self.config.parse(config)
   

