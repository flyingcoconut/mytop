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
Ui module
"""

import time
import curses
import sys
import os
import select
import collections

from mytop import session
from mytop import config
from mytop import drivers


class CursesUi(object):
    """The ui class"""
    def __init__(self):
        self.fullscreen = False
        self.sessions = session.SessionsManager()
        self.delay_counter = 0
        self.cursor_pos = 0
        self.scr = None
        self.cursor_pos_x = 0
        self.keymap = {"a": self.add_session,
                  "e": None,
                  "F": self.toggle_fullscreen,
                  "f": self.edit_filter,
                  "d": self.edit_delay,
                  "h": self.display_help,
                  "p": self.pause_session,
                  "q": self.quit,
                  "r": self.remove_current_session,
                  "w": self.write_to_file,
                  ":": self.command
        }

    @property
    def max_x(self):
        """Get maximum x position"""
        return self.scr.getmaxyx()[1]

    @property
    def max_y(self):
        """Get maximum y position"""
        return self.scr.getmaxyx()[0]

    def record(self):
        """Record a session"""
        pass

    def play(self):
        """Play a session"""
        pass

    def save_session(self):
        """Save session information"""
        pass

    def write_to_file(self):
        """Write process to file in a csv format"""
        path = self.ask("Write to : ")
        if os.path.isfile(path):
            resp = self.ask('File exist. Do you want to overwrite ? [y/N]')
            if resp != "y":
                return
        self.error("Need to be done")

    def edit_delay(self):
        """Edit session refresh delay"""
        if self.sessions.current is None:
            self.error("No current session")
        else:
            value = self.ask('Specify delay in second : ')
            try:
                delay = int(value)
                self.delay_counter = 0
                self.sessions.current.delay = delay
            except ValueError:
                self.error('Bad delay value')

    def command(self):
        """Command line"""
        commands = {"quit": self.quit,
                    "help": self.display_help,
                    "switch": self.switch_session,
                    "add": self.add_session,
                    "remove": self.remove_session
                    }
        response = [x.strip() for x in self.ask("command : ").split(" ")]
        command = response[0]
        args = response[1:]
        try:
            commands[command](*args)
        except KeyError:
            self.error(command + " : not found")

    def ask(self, question):
        """Ask question"""
        if self.fullscreen:
            ques_pos = self.max_y - 1
        else:
            ques_pos = 4
        self.scr.nodelay(0)
        curses.echo()
        curses.curs_set(1)
        self.scr.move(ques_pos, 0)
        self.scr.clrtoeol()
        self.scr.addstr(ques_pos, 0, question[:self.max_x])
        value = self.scr.getstr()
        return value.decode("utf-8")

    def error(self, error):
        """Ask question"""
        if self.fullscreen:
            ques_pos = self.max_y - 1
        else:
            ques_pos = 4
        curses.echo()
        self.scr.move(ques_pos, 0)
        self.scr.clrtoeol()
        self.scr.addstr(ques_pos, 0, error.ljust(self.max_x)[:self.max_x])
        self.scr.refresh()
        time.sleep(2)

    def add_session(self):
        """Add session"""
        value = self.ask("driver : ")
        try:
            driver = drivers.load(value)
        except ValueError:
            self.error("driver is not valid : " + value)
        except ImportError as error:
            self.error(str(error))
        else:
            configs = {}
            for conf in driver.config.configs:
                value = self.ask(conf.name + " : ")
                configs[conf.name] = value
            index = self.sessions.add(driver, configs)
            self.sessions.switch(index)


    def display_help(self):
        """Display help"""
        help_text = """
     Keyboard shortcut

     a: Add a new process manager
     c: Edit column display
     d: Modify delay between refresh
     e: Edit current connection
     f: Filter tops
     F: Display in fullscreen mode
     o: Open a saved session or a record
     p: Pause
     r: Remove current connection
     R: Record a session
     s: Save session
     w: Write process to a csv file
     h: Display this help
     H: Toggle history mode
     q: Quit
     :  Command

     Use up and down arrow to select process
        """
        self.scr.erase()
        self.scr.nodelay(0)
        curses.noecho()
        self.scr.addstr(1, 0, help_text)
        self.scr.addstr(self.max_y - 1, 1, "Press any key to quit")
        self.scr.refresh()
        self.scr.getch()

    def edit_session(self):
        """Edit a session"""
        pass

    def edit_filter(self):
        """Edit filter"""
        pass

    def display_header(self):
        """Display header info"""
        pass

    def display_footer(self):
        """Display footer informations"""
        informations = collections.OrderedDict()
        informations["Sessions"] = "0/0"
        informations["Driver"] = "None"
        informations["Status"] = "None"
        informations["History"] = "None"
        status = {session.STATUS_STOPPED: "Stopped",
                  session.STATUS_INITIALIZING: "Initializing",
                  session.STATUS_RUNNING: "Running",
                  session.STATUS_PAUSED: "Paused",
                  session.STATUS_ERROR: "Error"
                 }
        if self.sessions.current is not None:
            index = str(self.sessions.index + 1)
            informations["Sessions"] = index + "/" + str(len(self.sessions))
            informations["Driver"] = self.sessions.current.driver.name
            informations["Status"] = status[self.sessions.current.status]
            informations["History"] = str(len(self.sessions.current.history))
            if self.sessions.current.status == session.STATUS_ERROR:
                informations["Error"] = self.sessions.current.last_error
        self.scr.addstr(self.max_y-1, 0,
                        ", ".join("{!s} : {!s}".format(key,val)
                        for (key,val) in informations.items()).ljust(self.max_x - 1)[:self.max_x-1],
                        curses.A_BOLD | curses.A_REVERSE)

    def display_tops(self):
        """Display tops to screen"""
        #{k:v for (k,v) in d.items() if filter_string in k} filtering
        if self.fullscreen:
            cnt = 1
            max_process = self.max_y - 2
        else:
            cnt = 6
            max_process = self.max_y - 6

        if self.sessions.current is None:
            self.scr.hline(cnt-1, 0, " ",
                           self.max_x, curses.A_BOLD | curses.A_REVERSE)
            return

        column = [None] * len(config.DEFAULT_CONFIG["drivers"][self.sessions.current.driver.name]["process"].keys())
        titles = [None] * len(config.DEFAULT_CONFIG["drivers"][self.sessions.current.driver.name]["process"].keys())
        for key in config.DEFAULT_CONFIG["drivers"][self.sessions.current.driver.name]["process"].keys():
            position = config.DEFAULT_CONFIG["drivers"][self.sessions.current.driver.name]["process"][key]["position"]
            length = config.DEFAULT_CONFIG["drivers"][self.sessions.current.driver.name]["process"][key]["length"]
            alignment = config.DEFAULT_CONFIG["drivers"][self.sessions.current.driver.name]["process"][key]["alignment"]
            titles[position] = (config.DEFAULT_CONFIG["drivers"][self.sessions.current.driver.name]["process"][key]["title"])
            if alignment == "left":
                column[position] = "{: <" + str(length) + "." + str(length) + "}"
            elif alignment == "right":
                column[position] = "{: >" + str(length) + "." + str(length) + "}"
            elif alignment == "center":
                column[position] = "{: ^" + str(length) + "." + str(length) + "}"

        self.scr.addstr(cnt - 1 , 0, " ".join(column).format(*titles).ljust(self.max_x)[self.cursor_pos_x:self.max_x + self.cursor_pos_x], curses.A_BOLD|curses.A_REVERSE) #Display title bar
        try:
            sortby = config.DEFAULT_CONFIG["drivers"][self.sessions.current.driver.name]["sortby"]
            tops = sorted(self.sessions.current.history.last(),
                          key=lambda k: k[sortby], reverse=True)
        except KeyError:
            tops = self.sessions.current.history.last()
        for i in tops[self.cursor_pos:max_process + self.cursor_pos - 1]:
            informations = [None] * len(config.DEFAULT_CONFIG["drivers"][self.sessions.current.driver.name]["process"].keys())
            for key in config.DEFAULT_CONFIG["drivers"][self.sessions.current.driver.name]["process"].keys():
                position = config.DEFAULT_CONFIG["drivers"][self.sessions.current.driver.name]["process"][key]["position"]
                length = config.DEFAULT_CONFIG["drivers"][self.sessions.current.driver.name]["process"][key]["length"]
                try:
                    informations[position] = i[key]
                except KeyError:
                    informations[position] = ""
            informations = map(str, informations)
            self.scr.addstr(cnt, 0, " ".join(column).format(*informations)[self.cursor_pos_x:self.max_x + self.cursor_pos_x])
            cnt += 1

    def remove_session(self, index):
        """Remove current session"""
        try:
            self.sessions.remove(int(index) - 1)
        except session.SessionsManagerError as error:
            self.error(str(error))
        

    def remove_current_session(self):
        """Remove current session"""
        try:
            self.sessions.remove()
        except session.SessionsManagerError as error:
            self.error(str(error))

    def switch_session(self, index):
        try:
            self.sessions.switch(int(index) - 1)
        except session.SessionsManagerError:
            self.error("Session %d does not exist" % int(index))

    def pause_session(self):
        """Pause and Unpause session"""
        if self.sessions.current is None:
            self.error("No current session")
        else:
            self.sessions.current.pause()

    def toggle_fullscreen(self):
        if self.fullscreen:
            self.fullscreen = False
        else:
            self.fullscreen = True

    def handle_key(self):
        """Handle key input"""
        key = self.scr.getch()
        try:
            key = chr(key) #try to convert to ascii
        except ValueError:
            pass
        try:
            self.keymap[key]()
        except KeyError:
            pass
        if key in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            #All keyboard key number are used to select wich connection to display
            index = int(key)
            self.switch_session(index)
        elif key == curses.KEY_LEFT:
            if self.cursor_pos_x > 0:
                self.cursor_pos_x -= 5
        elif key == curses.KEY_RIGHT:
            self.cursor_pos_x += 5
        elif key == curses.KEY_DOWN:
            self.cursor_pos = self.cursor_pos + 1
        elif key == curses.KEY_UP:
            if self.cursor_pos > 0:
                self.cursor_pos = self.cursor_pos - 1

    def start(self):
        """Wrap function if bug happen, then reset terminal properly"""
        curses.wrapper(self.start_ui)

    def quit(self):
        """Stop all sessions and quit"""
        self.sessions.stop()
        sys.exit(0)

    def refresh(self):
        """Refresh screen and all elements"""
        self.scr.erase()
        self.scr.nodelay(1)
        self.scr.keypad(1)
        curses.curs_set(0)
        curses.noecho()
        if self.fullscreen:
            self.display_tops()
            self.display_footer()
        else:
            self.display_header()
            self.display_tops()
            self.display_footer()
        self.scr.refresh()

    def start_color(self):
        try:
            curses.use_default_colors()
            curses.start_color()
        except curses.error:
            pass

    def start_ui(self, scr):
        """The main function loop"""
        self.scr = scr #Set screen
        self.start_color()
        self.refresh()
        while 1:
            if self.sessions.current is None:
                delay = None
            else:
                delay = self.sessions.current.delay
            try:
                select.select([sys.stdin], [], [], delay) #Wait for input
            except select.error:
                pass
            self.handle_key()
            self.refresh()
