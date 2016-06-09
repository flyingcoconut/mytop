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

import json
import selectors
import sys
import os
import argparse

from mytop import configparser
from mytop import version

class DriverError(Exception):
    def __init__(self, message):
        self.message = message

class UnknownError(Exception):
    def __init__(self, exception):
        self.errorno = 0
        self.message = "Unknow error: " + str(exception)

class UnicodeError(Exception):
    def __init__(self):
        self.errorno = 1
        self.message = "Invalid unicode"

class SerializeError(Exception):
    def __init__(self):
        self.errorno = 2
        self.message = "Impossible to serialize message"

class InvalidMethodError(Exception):
    def __init__(self, method):
        self.errorno = 3
        self.message = "Invalid call: " + method

class InvalidCallError(Exception):
    def __init__(self):
        self.errorno = 4
        self.message = "Invalid call format"

class InvalidParamsError(Exception):
    def __init__(self, **params):
        self.errorno = 5
        self.message = "Invalid params: " + ", ".join(params.keys())

class InvalidConfigError(Exception):
    def __init__(self, name, validator, default, required):
        self.errorno = 6
        self.message = "Invalid config"

class UnconfiguredError(Exception):
    def __init__(self):
        self.errorno = 7
        self.message = "Driver not configured before initialization"

class NotImplementedError(Exception):
    def __init__(self):
        self.errorno = 8
        self.message = ""

class TimeoutError(Exception):
    def __init__(self):
        self.errorno = 9
        self.message = ""

class Driver(object):
    STATE_UNCONFIGURED = "unconfigured"
    STATE_CONFIGURED = "configured"
    STATE_INITIALIZE = "initialized"
    STATE_TERMINATED = "terminated"
    STATE_ERROR = "error"
    def __init__(self, name=None, description=None, version=None, author=None, collector=None):
        self.name = name
        self.description = description
        self.version = version
        self.author = author
        self.collector = collector
        self.status = Driver.STATE_UNCONFIGURED
        self.running = False
        self._args_parser = argparse.ArgumentParser(description=description)
        self._args_parser.add_argument("--name", action="store_true", help="Display driver name")
        self._args_parser.add_argument("--description", action="store_true", help="Display driver description")
        self._args_parser.add_argument("--author", action="store_true", help="Display driver author")
        self._args_parser.add_argument("--version", action="store_true", help="Display driver version")
        self._args_parser.add_argument("--cli", action="store_true")
        self._selector = selectors.DefaultSelector()
        self._conf = configparser.ConfigParser()
        self._calls = {
            "listmetrics": self._handle_listmetrics,
            "enablemetric": None,
            "disablemetric": None,
            "listactions": None,
            "action": None,
            "collect": self._handle_collect,
            "init": self._handle_init,
            "term": self._handle_term,
            "status": self._handle_status,
            "info": self._handle_info,
            "setconfigs": self._handle_setconfigs,
            "getconfigs": self._handle_getconfigs
        }

    def add_config(self, name, validator, default=None, choices=[], required=False):
        self._conf.add_config(name, validator, default, choices, required)

    def start(self):
        """Start a selector and register stdin fd"""
        self._parse_args()
        self._selector.register(sys.stdin, selectors.EVENT_READ, self._recv_rpc_call)
        self.running = True
        while self.running:
            try:
                events = self._selector.select(timeout=1)
            except KeyboardInterrupt:
                sys.exit()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
        sys.exit()

    def _handle_setconfigs(self, configs={}):
       """Handle setconfigs rpc call"""
       self.status = Driver.STATE_CONFIGURED

    def _handle_getconfigs(self):
       """Handle setconfigs rpc call"""
       pass

    def _handle_init(self):
       """Handle init rpc call"""
       if self.status is Driver.STATE_UNCONFIGURED:
           raise UnconfiguredError()
       self.collector.initialize()
       self.status = Driver.STATE_INITIALIZE
           
    def _handle_term(self):
       """Handle term rpc call"""
       self.running = False

    def _handle_status(self):
       """Handle term rpc call"""
       return self.status

    def _handle_info(self):
        info = {
            "name": self.name,
            "description": self.description,
            "driver_version": self.version,
            "author": self.author,
            "mytop_version": version.version
        }
        return info

    def _handle_listmetrics(self):
       """Handle term rpc call"""
       return self.collector.list_metrics()

    def _handle_collect(self):
       """Handle term rpc call"""
       try:
           metrics = self.collector.collect()
       except Exception as e:
           raise UnknownError(e)
       return metrics

    def _parse_args(self):
        args = self._args_parser.parse_args()
        if args.name:
            print(self.name)
            sys.exit()
        elif args.description:
            print(self.description)
            sys.exit()

    def _serialize_error(self, exception):
        error = {
            "err": exception.errorno,
            "msg": exception.message
        }
        return error

    def _serialize_call(self, data):
        try:
            data = data.decode("utf-8")
        except UnicodeEncodeError:
            raise UnicodeError()
        try:
            serialize = json.loads(data)
        except ValueError as e:
            raise SerializeError()

        try:
            method = serialize["method"]
            params = serialize["params"]
        except KeyError:
            raise InvalidCallError()
        try:
            try:
               result = self._calls[method](**params)
            except TypeError:
               raise InvalidParamsError(**params)
        except KeyError:
            raise InvalidMethodError(method)
        return result
            

    def _recv_rpc_call(self, conn, mask):
        data = os.read(sys.stdin.fileno(), 1024)
        try:
            result = self._serialize_call(data)
        except UnknownError as e:
            error = self._serialize_error(e)
            print(json.dumps(error))
            return
        except SerializeError as e:
            error = self._serialize_error(e)
            print(json.dumps(error))
            return
        except InvalidCallError as e:
            error = self._serialize_error(e)
            print(json.dumps(error))
            return
        except InvalidMethodError as e:
            error = self._serialize_error(e)
            print(json.dumps(error))
            return
        except InvalidParamsError as e:
            error = self._serialize_error(e)
            print(json.dumps(error))
            return
        except UnconfiguredError as e:
            error = self._serialize_error(e)
            print(json.dumps(error))
            return

        resp = {
            "result": result
        }
        print(json.dumps(resp))
        
