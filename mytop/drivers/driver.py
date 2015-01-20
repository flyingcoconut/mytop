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
"""
Base Class Driver
"""

import logging

class DriverError(Exception):
    """Driver error class"""
    pass

class Config(object):
    """Config class"""
    def __init__(self, name, default, required, validator):
        self.name = name
        self.default = default
        self.required = required
        self.validator = validator

class DriverConfig(object):
    """
    Driver config class
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.configs = []

    def add(self, name, default=None, required=True, validator=None):
        conf = Config(name, default, required, validator)
        self.configs.append(conf)

    def parse(self, config):
        """Parse config"""
        for i in self.configs:
            if i.name in config:
                if i.validator:
                    #Validate
                    try:
                        value = i.validator(config[i.name])
                    except:
                        raise DriverError("Impossible to validate : " + str(key) + " value : " + str(config[key]))
                    else:
                        setattr(self, i.name, value)
                else:
                    setattr(self, i.name, value)
            else:
                if i.required:
                    #Verify if required
                    raise DriverError("Configuration key : " + i.name + " is required")
                else:
                    setattr(self, i.name, i.default)

class Driver(object):
    """
    Base class Driver
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
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
