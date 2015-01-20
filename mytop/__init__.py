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

import time
import zlib
import pickle
import threading
import logging


class History(object):
    def __init__(self, lenght=0):
        self.lenght = lenght
        self._items = []
        self._timeline = {}

    def add(self, items):
        """Add a frame"""
        compressed = zlib.compress(pickle.dumps(items))
        self._items.append(compressed)

    def last(self):
        """Return last frame"""
        try:
            items = pickle.loads(zlib.decompress(self._items[-1]))
        except IndexError:
            items = []
        return items

    def first(self):
        """Return first frame"""
        pass

    def __len__(self):
        return len(self._items)

class Session(threading.Thread):
    STATUS_STOPPED = 0
    STATUS_INITIALIZING = 1
    STATUS_RUNNING = 2
    STATUS_PAUSED = 3
    STATUS_ERROR = 4
    def __init__(self, driver, config, history=10):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.daemon = True
        self.driver = driver
        self.config = config
        self.filters = []
        self.history = History(history)
        self.delay = 3
        self.status = self.STATUS_STOPPED
        self.last_error = None

    def run(self):
        """Start the session"""
        self.logger.debug("Starting the session")
        self.status = self.STATUS_INITIALIZING
        try:
            self.driver.configure(self.config)
            self.driver.initialize()
        except Exception as error:
            self.status = self.STATUS_ERROR
            self.last_error = str(error)
        self.status = self.STATUS_RUNNING
        while (self.status == self.STATUS_RUNNING):
            try:
                self.history.add(self.driver.tops())
            except Exception as error:
                self.status = self.STATUS_ERROR
                self.last_error = str(error)
            time.sleep(self.delay)

    def stop(self):
        """Stop the session"""
        self.status = self.STATUS_STOPPED
        self.driver.terminate()

    def pause(self):
        """Pause the session"""
        self.status = self.STATUS_PAUSED

    def resume(self):
        """Resume the session"""
        pass

    def record(self):
        """Record a session"""
        pass

    def tops(self):
        items = self.driver.tops()
        #self.history.add(items)
        return items

    def fields(self):
        return self.driver.fields()

    def info(self):
        return self.driver.info()

    def additional(self):
        pass

class ConfigError(Exception):
    """
    Config error class
    """
    def __init__(self, value):
        self.value = value
        Exception.__init__(self, value)
    def __str__(self):
        return repr(self.value)

default_config = {
    "drivers": {
        "mysql": {
            "process": {
                "info": {
                    "position": 6,
                    "length": 40,
                    "alignment": "left",
                    "title": "Info"
                },
                "pid": {
                    "position": 0,
                    "length": 10,
                    "alignment": "right",
                    "title": "Pid"
                },
                "db": {
                    "position": 3,
                    "length": 20,
                    "alignment": "left",
                    "title": "Database"
                },
                "state": {
                    "position": 4,
                    "length": 7,
                    "alignment": "left",
                    "title": "State"
                },
                "host": {
                    "position": 2,
                    "length": 15,
                    "alignment": "left",
                    "title": "Hostname"
                },
                "user": {
                    "position": 1,
                    "length": 11,
                    "alignment": "left",
                    "title": "Username"
                },
                "time": {
                    "position": 5,
                    "length": 8,
                    "alignment": "left",
                    "title": "Uptime"
                }
            },
            "headers": {}
        },
        "linux:process": {
            "process": {
                "pid": {
                    "position": 0,
                    "length": 5,
                    "alignment": "right",
                    "title": "PID"
                },
                "user": {
                    "position": 1,
                    "length": 9,
                    "alignment": "left",
                    "title": "USER"
                },
                "nice": {
                    "position": 2,
                    "length": 2,
                    "alignment": "right",
                    "title": "NI"
                },
                "vms": {
                    "position": 3,
                    "length": 7,
                    "alignment": "right",
                    "title": "VIRT"
                },
                "rss": {
                    "position": 4,
                    "length": 6,
                    "alignment": "right",
                    "title": "RES"
                },
                "shared": {
                    "position": 5,
                    "length": 6,
                    "alignment": "right",
                    "title": "SHR"
                },
                "state": {
                    "position": 6,
                    "length": 1,
                    "alignment": "right",
                    "title": "S"
                },
                "cpu": {
                    "position": 7,
                    "length": 4,
                    "alignment": "right",
                    "title": "%CPU"
                },
                "memory": {
                    "position": 8,
                    "length": 4,
                    "alignment": "right",
                    "title": "%MEM"
                },
                "time": {
                    "position": 9,
                    "length": 8,
                    "alignment": "right",
                    "title": "TIME+"
                },
                "command": {
                    "position": 10,
                    "length": 10,
                    "alignment": "left",
                    "title": "COMMAND"
                }
            },
            "sortby" : "cpu"
        },
        "linux:network": {
            "process": {
                "interface": {
                    "position": 0,
                    "length": 9,
                    "alignment": "left",
                    "title": "INTERFACE"
                },
                "packets_sent": {
                    "position": 1,
                    "length": 5,
                    "alignment": "right",
                    "title": "PKG S"
                },
                "packets_recv": {
                    "position": 2,
                    "length": 5,
                    "alignment": "right",
                    "title": "PKG R"
                },
                "bytes_sent": {
                    "position": 3,
                    "length": 7,
                    "alignment": "right",
                    "title": "BYTES S"
                },
                "bytes_recv": {
                    "position": 4,
                    "length": 7,
                    "alignment": "right",
                    "title": "BYTES R"
                },
                "dropout": {
                    "position": 5,
                    "length": 6,
                    "alignment": "right",
                    "title": "DROP O"
                },
                "dropin": {
                    "position": 6,
                    "length": 6,
                    "alignment": "right",
                    "title": "DROP I"
                },
                "errout": {
                    "position": 7,
                    "length": 5,
                    "alignment": "right",
                    "title": "ERR O"
                },
                "errin": {
                    "position": 8,
                    "length": 5,
                    "alignment": "right",
                    "title": "ERR I"
                }
            },
            "headers": {}
        },
        "linux:disk": {
            "process": {
                "device": {
                    "position": 0,
                    "length": 6,
                    "alignment": "left",
                    "title": "DEVICE"
                },
                "read_bytes": {
                    "position": 1,
                    "length": 6,
                    "alignment": "right",
                    "title": "READ B"
                },
                "write_bytes": {
                    "position": 2,
                    "length": 7,
                    "alignment": "right",
                    "title": "WRITE B"
                },
                "read_time": {
                    "position": 3,
                    "length": 6,
                    "alignment": "right",
                    "title": "READ T"
                },
                "write_time": {
                    "position": 4,
                    "length": 7,
                    "alignment": "right",
                    "title": "WRITE T"
                },
                "read_count": {
                    "position": 5,
                    "length": 6,
                    "alignment": "right",
                    "title": "READ C"
                },
                "write_count": {
                    "position": 6,
                    "length": 7,
                    "alignment": "right",
                    "title": "WRITE C"
                },
                "mountpoint": {
                    "position": 7,
                    "length": 10,
                    "alignment": "left",
                    "title": "MOUNT"
                },
                "fstype": {
                    "position": 8,
                    "length": 4,
                    "alignment": "left",
                    "title": "FS"
                },
                "opts": {
                    "position": 9,
                    "length": 20,
                    "alignment": "left",
                    "title": "OPTS"
                }
            },
            "headers": {}
        },
        "linux:socket": {
            "process": {
                "fd": {
                    "position": 0,
                    "length": 2,
                    "alignment": "right",
                    "title": "FD"
                },
                "family": {
                    "position": 1,
                    "length": 10,
                    "alignment": "left",
                    "title": "FAMILY"
                },
                "type": {
                    "position": 2,
                    "length": 6,
                    "alignment": "left",
                    "title": "TYPE"
                },
                "laddr": {
                    "position": 3,
                    "length": 20,
                    "alignment": "left",
                    "title": "LADDR"
                },
                "raddr": {
                    "position": 4,
                    "length": 20,
                    "alignment": "left",
                    "title": "RADDR"
                },
                "status": {
                    "position": 5,
                    "length": 10,
                    "alignment": "left",
                    "title": "STATUS"
                },
                "pid": {
                    "position": 6,
                    "length": 7,
                    "alignment": "right",
                    "title": "PID"
                }
            },
            "headers": {}
        },
        "linux:cpu": {
            "process": {
                "cpu": {
                    "position": 0,
                    "length": 4,
                    "alignment": "right",
                    "title": "CPU"
                },
                "user": {
                    "position": 1,
                    "length": 6,
                    "alignment": "right",
                    "title": "%USER"
                },
                "nice": {
                    "position": 2,
                    "length": 6,
                    "alignment": "right",
                    "title": "%NICE"
                },
                "system": {
                    "position": 3,
                    "length": 6,
                    "alignment": "right",
                    "title": "%SYS"
                },
                "idle": {
                    "position": 4,
                    "length": 6,
                    "alignment": "right",
                    "title": "%IDLE"
                },
                "iowait": {
                    "position": 5,
                    "length": 7,
                    "alignment": "right",
                    "title": "%IOWAIT"
                },
                "irq": {
                    "position": 6,
                    "length": 6,
                    "alignment": "right",
                    "title": "%IRQ"
                },
                "softirq": {
                    "position": 7,
                    "length": 8,
                    "alignment": "right",
                    "title": "%SOFTIRQ"
                },
                "steal": {
                    "position": 8,
                    "length": 6,
                    "alignment": "right",
                    "title": "%STEAL"
                },
                "guest": {
                    "position": 9,
                    "length": 6,
                    "alignment": "right",
                    "title": "%GUEST"
                },
                "guest_nice": {
                    "position": 10,
                    "length": 11,
                    "alignment": "right",
                    "title": "%GUEST NICE"
                }

            },
            "headers": {}
        },
        "apache": {
            "process": {
                "server": {
                    "position": 0,
                    "length": 5,
                    "alignment": "right",
                    "title": "Srv"
                },
                "pid": {
                    "position": 1,
                    "length": 9,
                    "alignment": "right",
                    "title": "PID"
                },
                "access": {
                    "position": 2,
                    "length": 13,
                    "alignment": "left",
                    "title": "Acc"
                },
                "mode": {
                    "position": 3,
                    "length": 1,
                    "alignment": "left",
                    "title": "M"
                },
                "cpu": {
                    "position": 4,
                    "length": 6,
                    "alignment": "left",
                    "title": "CPU"
                },
                "seconds": {
                    "position": 5,
                    "length": 6,
                    "alignment": "right",
                    "title": "SS"
                },
                "required": {
                    "position": 6,
                    "length": 1,
                    "alignment": "right",
                    "title": "Req"
                },
                "connection": {
                    "position": 7,
                    "length": 4,
                    "alignment": "right",
                    "title": "Conn"
                },
                "child": {
                    "position": 8,
                    "length": 5,
                    "alignment": "right",
                    "title": "Child"
                },
                "slot": {
                    "position": 9,
                    "length": 5,
                    "alignment": "right",
                    "title": "Slot"
                },
                "client": {
                    "position": 10,
                    "length": 11,
                    "alignment": "left",
                    "title": "Client"
                },
                "vhost": {
                    "position": 11,
                    "length": 25,
                    "alignment": "left",
                    "title": "VHost"
                },
                "request": {
                    "position": 12,
                    "length": 40,
                    "alignment": "left",
                    "title": "Request"
                }
            },
            "headers": {}
        },
        "elasticsearch": {
            "process": {
                "index": {
                    "position": 0,
                    "length": 20,
                    "alignment": "left",
                    "title": "INDEX"
                },
                "size": {
                    "position": 1,
                    "length": 5,
                    "alignment": "right",
                    "title": "SIZE"
                },
                "max_doc": {
                    "position": 2,
                    "length": 5,
                    "alignment": "right",
                    "title": "MAX"
                },
                "num_doc": {
                    "position": 3,
                    "length": 5,
                    "alignment": "right",
                    "title": "NUM"
                },
                "deleted_doc": {
                    "position": 4,
                    "length": 5,
                    "alignment": "right",
                    "title": "DEL"
                },
                "merges_total_docs": {
                    "position": 5,
                    "length": 6,
                    "alignment": "right",
                    "title": "MTOTAL"
                },
                "merges_total_size": {
                    "position": 6,
                    "length": 5,
                    "alignment": "right",
                    "title": "MSIZE"
                },
                "merges_current_docs": {
                    "position": 7,
                    "length": 12,
                    "alignment": "right",
                    "title": "MCURDOCS"
                },
                "merges_current": {
                    "position": 8,
                    "length": 5,
                    "alignment": "right",
                    "title": "MCUR"
                },
                "merges_total_time": {
                    "position": 9,
                    "length": 9,
                    "alignment": "right",
                    "title": "MTOTALTIME"
                },
                "merges_total": {
                    "position": 10,
                    "length": 6,
                    "alignment": "right",
                    "title": "MTOTAL"
                },
                "shards": {
                    "position": 11,
                    "length": 6,
                    "alignment": "right",
                    "title": "SHARDS"
                },
                "refresh_total_time": {
                    "position": 12,
                    "length": 10,
                    "alignment": "right",
                    "title": "RTOTALTIME"
                },
                "refresh_total": {
                    "position": 13,
                    "length": 6,
                    "alignment": "right",
                    "title": "RTOTAL"
                },
                "flush_total_time": {
                    "position": 14,
                    "length": 10,
                    "alignment": "right",
                    "title": "FTOTALTIME"
                },
                "flush_total": {
                    "position": 15,
                    "length": 6,
                    "alignment": "right",
                    "title": "FTOTAL"
                }
            },
            "sortby": "num_doc"
        }
    }
}
