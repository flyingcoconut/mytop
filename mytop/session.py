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
Session Module
"""

import time
import zlib
import pickle
import threading
import logging

class SessionError(Exception):
    """Driver error class"""
    pass

class SessionsManagerError(Exception):
    """Driver error class"""
    pass

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

class SessionsManager(object):
    """Manage sessions"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.sessions = []
        self.current = None

    def add(self, driver, configs):
        new_session = Session(driver, configs)
        new_session.start()
        self.sessions.append(new_session)
        return self.sessions.index(new_session)

    def remove(self):
        if self.current is None:
            raise SessionsManagerError("Session does not exist")
        else:
            self.current.stop()
            index = self.sessions.index(self.current)
            self.sessions.remove(self.current)
            if index > len(self.sessions) - 1:
                try:
                    self.current = self.sessions[-1]
                except IndexError:
                    self.current = None
            else:
                self.current = self.sessions[index - 1]

    def switch(self, index):
        try:
            self.current = self.sessions[index]
        except IndexError:
            raise SessionsManagerError("Session %d does not exist" % index)

    def stop(self):
        """Stop the session"""
        pass

    def pause(self):
        """Pause the session"""
        pass

    def resume(self):
        """Resume the session"""
        pass

    def record(self):
        """Record a session"""
        pass

    def tops(self):
        pass

    def fields(self):
        pass

    def info(self):
        pass

    def additional(self):
        pass

    @property
    def index(self):
        if self.current is None:
            return None
        else:
            return self.sessions.index(self.current)
    @property
    def delay(self):
        if self.current is None:
            return None
        else:
            return self.current.delay

    @property
    def driver(self):
        if self.current is None:
            return None
        else:
            return self.current.driver

    @property
    def last_error(self):
        if self.current is None:
            return None
        else:
            return self.current.last_error

    @property
    def status(self):
        if self.current is None:
            return None
        else:
            return self.current.status

    @property
    def history(self):
        if self.current is None:
            return None
        else:
            return self.current.history

    def __iter__(self):
        """Iterate sessions"""
        for session in self.sessions:
            yield session

    def __len__(self):
        """Return the number of sessions"""
        return len(self.sessions)
