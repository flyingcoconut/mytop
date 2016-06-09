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

class Config(object):
    def __init__(self, name, validator, default=None, choices=[]):
        self.name = name
        self.validator = validator
        self.default = default
        self.choices = choices
        self.value = None

    def validate(self, value):
        """Validate config with value"""
        pass

    def dump(self):
        conf = {}
        conf["validator"] = self.validator
        conf["default"] = self.default
        conf["choices"] = self.choices
        conf["value"] = self.value
        return conf

class ConfigParser(object):
    def __init__(self):
        self.configs = {}

    def add_config(self, name, validator, default=None, choices=[], required=False):
        """Add a new configuration"""
        conf = Config(name, validator, default, choices)
        self.configs[name] = conf

    def validate(self):
        """Validate all configurations"""
        pass

    def dump(self):
        configs = {}
        for c in self.configs:
            configs[c] = self.configs[c].dump()
        return configs
