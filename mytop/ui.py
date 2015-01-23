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
        if os.path.exists(path) & os.path.isfile(path):
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
                self.sessions.delay = delay
            except ValueError:
                self.error('Bad delay value')

    def command(self):
        """Get manual command"""
        command = self.ask("command : ")
        if command == "quit":
            sys.exit(0)

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
        informations = []
        if self.sessions.current is None:
            informations.append("Sessions : 0/" + str(len(self.sessions)))
            informations.append("Driver : None")
            informations.append("Status : None")
            informations.append("History : None")
        else:
            index = str(self.sessions.index + 1)
            informations.append("Sessions : " + index + "/" \
                                + str(len(self.sessions)))
            informations.append("Driver : " + self.sessions.driver.name)
            if self.sessions.status == session.Session.STATUS_STOPPED:
                informations.append("Status : Stopped")
            elif self.sessions.status ==  session.Session.STATUS_INITIALIZING:
                informations.append("Status : Initializing")
            elif self.sessions.status == session.Session.STATUS_RUNNING:
                informations.append("Status : Running")
            elif self.sessions.status == session.Session.STATUS_PAUSED:
                informations.append("Status : Paused")
            elif self.sessions.status == session.Session.STATUS_ERROR:
                informations.append("Status : Error")
            informations.append("History : " + str(len(self.sessions.history)))
            if self.sessions.status == session.Session.STATUS_ERROR:
                informations.append("Error : " + self.sessions.last_error)
        self.scr.addstr(self.max_y-1, 0, ", ".join(informations).ljust(self.max_x - 1)[:self.max_x-1], curses.A_BOLD | curses.A_REVERSE)

    def display_tops(self):
        """Display tops to screen"""
        #{k:v for (k,v) in d.items() if filter_string in k} filtering
        if self.fullscreen:
            cnt = 1
            max_process = self.max_y - 2
        else:
            cnt = 6
            max_process = self.max_y - 6

        if self.sessions.current == None:
            self.scr.hline(cnt-1, 0, " ", self.max_x, curses.A_BOLD | curses.A_REVERSE)
            return

        column = [None] * len(config.DEFAULT_CONFIG["drivers"][self.sessions.driver.name]["process"].keys())
        titles = [None] * len(config.DEFAULT_CONFIG["drivers"][self.sessions.driver.name]["process"].keys())
        for key in config.DEFAULT_CONFIG["drivers"][self.sessions.driver.name]["process"].keys():
            position = config.DEFAULT_CONFIG["drivers"][self.sessions.driver.name]["process"][key]["position"]
            length = config.DEFAULT_CONFIG["drivers"][self.sessions.driver.name]["process"][key]["length"]
            alignment = config.DEFAULT_CONFIG["drivers"][self.sessions.driver.name]["process"][key]["alignment"]
            titles[position] = (config.DEFAULT_CONFIG["drivers"][self.sessions.driver.name]["process"][key]["title"])
            if alignment == "left":
                column[position] = "{: <" + str(length) + "." + str(length) + "}"
            elif alignment == "right":
                column[position] = "{: >" + str(length) + "." + str(length) + "}"
            elif alignment == "center":
                column[position] = "{: ^" + str(length) + "." + str(length) + "}"

        self.scr.addstr(cnt - 1 , 0, " ".join(column).format(*titles).ljust(self.max_x)[self.cursor_pos_x:self.max_x + self.cursor_pos_x], curses.A_BOLD|curses.A_REVERSE) #Display title bar
        try:
            sortby = config.DEFAULT_CONFIG["drivers"][self.sessions.driver.name]["sortby"]
            tops = sorted(self.sessions.history.last(), key=lambda k: k[sortby], reverse=True)
        except KeyError:
            tops = self.sessions.history.last()
        for i in tops[self.cursor_pos:max_process + self.cursor_pos - 1]:
            informations = [None] * len(config.DEFAULT_CONFIG["drivers"][self.sessions.driver.name]["process"].keys())
            for key in config.DEFAULT_CONFIG["drivers"][self.sessions.driver.name]["process"].keys():
                position = config.DEFAULT_CONFIG["drivers"][self.sessions.driver.name]["process"][key]["position"]
                length = config.DEFAULT_CONFIG["drivers"][self.sessions.driver.name]["process"][key]["length"]
                try:
                    informations[position] = i[key]
                except KeyError:
                    informations[position] = ""
            informations = map(str, informations)
            self.scr.addstr(cnt, 0, " ".join(column).format(*informations)[self.cursor_pos_x:self.max_x + self.cursor_pos_x])
            cnt += 1

    def remove_session(self):
        """Stop and remove current session"""
        try:
            self.sessions.remove()
        except session.SessionsManagerError as error:
            self.error(str(error))

    def switch_session(self, index):
        try:
            self.sessions.switch(index - 1)
        except session.SessionsManagerError:
            self.error("Session %d does not exist" % index)

    def handle_key(self):
        """Handle key input"""
        key = self.scr.getch()
        if key == ord("a"):
            self.add_session()
        elif key == ord(":"):
            self.command()
        elif key == ord("F"):
            if self.fullscreen:
                self.fullscreen = False
            else:
                self.fullscreen = True
        elif key in [ord("1"), ord("2"), ord("3"), ord("4"), ord("5"), ord("6"), ord("7"), ord("8"), ord("9")]:
            #All keyboard key number are used to select wich connection to display
            index = int(chr(key))
            self.switch_session(index)
        elif key == ord("q"):
            #Key to exit mytop
            self.quit()
        elif key == ord("h"):
            self.display_help()
        elif key == curses.KEY_LEFT:
            if self.cursor_pos_x > 0:
                self.cursor_pos_x -= 5
        elif key == curses.KEY_RIGHT:
            self.cursor_pos_x += 5
        elif key == ord("d"):
            #Key to change delay
            self.edit_delay()
        elif key == ord("e"):
            #Key to edit the current connection
            pass
        elif key == ord("f"):
            #key to edit or add filter
            self.edit_filter()
        elif key == ord("w"):
            #Key to write results to a file
            self.write_to_file()
        elif key == curses.KEY_DOWN:
            self.cursor_pos = self.cursor_pos + 1
        elif key == curses.KEY_UP:
            if self.cursor_pos > 0:
                self.cursor_pos = self.cursor_pos - 1
        elif key == ord("p"):
            #Key to pause a session
            if self.sessions.current is None:
                self.error("No current session")
            else:
                self.sessions.current.pause()
        elif key == ord("r"):
            #Remove a session
            self.remove_session()
        else:
            pass

    def start(self):
        """Wrappe function if bug happen, then reset terminal properly"""
        curses.wrapper(self.start_ui)

    def quit(self):
        """Stop all sessions and quit"""
        for sess in self.sessions:
            sess.stop()
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
                delay = self.sessions.delay
            try:
                select.select([sys.stdin], [], [], delay) #Wait for input
            except select.error:
                pass
            self.handle_key()
            self.refresh()
