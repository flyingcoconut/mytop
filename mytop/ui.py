#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Patrick Charron
# Email : patrick.charron.pc@gmail.com
# Description : Tops viewer
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
import curses
import datetime
import sys

import mytop
from mytop import drivers

class Ui(object):
    """The ui class"""
    def __init__(self, session = None):
        self.fullscreen = False
        self.extension = False
        self.sessions = []
        self.current_session = None
        self.delay_counter = 1
        self.delay = 1
        self.paused = False
        self.history = False
        self.history_pos = 0
        self.cursor_pos = 0
        self.cursor_max_pos = 0
        self.scr = None
        self.cursor_pos_x = 0

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
        scr.addstr(3, 0, 'Write to : ')
        scr.move(3, 11)
        scr.nodelay(0)
        curses.echo()
        scr.refresh()
        path = scr.getstr()
        if os.path.exists(path) & os.path.isfile(path):
            scr.move(3, 0)
            scr.clrtoeol()
            curses.noecho()
            curses.curs_set(0)
            scr.addstr(3, 0, 'File exist. Do you want to overwrite ? [y/N]')
            resp = scr.getch()
            if resp == ord("y"):
                scr.refresh()
                try :
                    output_file = open(path, "w")
                    output_file.write("Id;User;Host;Db;State;Time;Info\n")
                    for process in pm.process:
                        line = str(process.pid) + ";" + process.user + ";" + process.host + ";" + process.db + ";" + process.state + ";" + str(process.time) + ";" + process.info
                        output_file.write(line + "\n")
                    output_file.close()
                except IOError:
                    scr.move(3, 0)
                    scr.clrtoeol()
                    scr.addstr(3, 0, 'Impossible to write file')
                    scr.refresh()
                    time.sleep(1)
        else:
            try :
                output_file = open(path, "w")
                output_file.write("Id;User;Host;Db;State;Time;Info\n")
                for process in pm.process:
                    line = str(process.pid) + ";" + process.user + ";" + process.host + ";" + process.db + ";" + process.state + ";" + str(process.time) + ";" + process.info
                    output_file.write(line + "\n")
                output_file.close()
            except IOError:
                scr.move(3, 0)
                scr.clrtoeol()
                scr.addstr(3, 0, 'Impossible to write file')
                scr.refresh()
                time.sleep(1)
        curses.noecho()
        curses.curs_set(1)
        scr.nodelay(1)
        scr.refresh()

    def edit_delay(self):
        value = self.ask('Specify delay in second : ')
        try:
            delay = int(value)
        except ValueError:
            self.error('Bad delay value')
        else:
            self.delay_counter = delay
            self.delay = delay

    def command(self):
        command = self.ask("command : ")
        if command == "quit":
            sys.exit(0)

    def ask(self, question):
        """Ask question"""
        (max_y, max_x) = self.scr.getmaxyx()
        if self.fullscreen:
             ques_pos = max_y - 1
        else:
             ques_pos = 3
        self.scr.nodelay(0)
        curses.echo()
        self.scr.move(ques_pos, 0)
        self.scr.clrtoeol()
        self.scr.addstr(ques_pos, 0, question[:max_x])
        value = self.scr.getstr()
        return value

    def error(self, error):
        """Ask question"""
        (max_y, max_x) = self.scr.getmaxyx()
        if self.fullscreen:
             ques_pos = max_y - 1
        else:
             ques_pos = 3
        self.scr.nodelay(0)
        curses.echo()
        self.scr.move(ques_pos, 0)
        self.scr.clrtoeol()
        self.scr.addstr(ques_pos, 0, error.ljust(max_x)[:max_x])
        self.scr.refresh()
        time.sleep(1)

    def add_session(self):
        """Add session"""
        value = self.ask("driver : ")
        if value != "":
            if value in drivers.list_drivers():
                driver = drivers.load(value)
            else:
                self.error('driver is not valid')
                return
        configs = {}
        for conf in driver.config.configs:
            value = self.ask(conf.name + " : ")
            configs[conf.name] = value
        session = mytop.Session(driver, configs)
        session.start()
        self.sessions.append(session)
        self.current_session = session


    def display_help(self):
        """Display help"""
        help_text = """
     Keyboard shortcut

     [a]dd          Add a new process manager
     [c]olumn       Edit column display
     [d]elay        Modify delay between refresh
     [e]dit         Edit current connection
     [f]ilter       Filter tops
     [F]ullscreen   Display in fullscreen mode
     [o]pen         Open a saved session or a record
     [p]aused       Pause
     [r]emove       Remove current connection
     [R]ecord       Record a session
     [s]ave         Save session
     [w]rite        Write process to a csv file
     [h]elp         Display this help
     [q]uit         Quit
     [:]            Command

     Use up and down arrow to select process
        """
        (max_y, max_x) = self.scr.getmaxyx()
        self.scr.erase()
        self.scr.nodelay(0)
        curses.noecho()
        self.scr.addstr(1, 0, help_text)
        self.scr.addstr(max_y - 1, 1, "Press any key to quit")
        self.scr.getch()
        self.scr.nodelay(1)
        curses.noecho()

    def display_history(self, key):
        #Key to navigate history
        if len(self.pms[self.pm_index]._history) == 0:
            self.scr.addstr(3, 0, 'No history')
            time.sleep(1)
        elif self.history:
            if key == curses.KEY_LEFT:
                if self.history_pos != 0:
                    self.history_pos = self.history_pos - 1
                    self.pms[self.pm_index].history(self.history_pos)
            if key == curses.KEY_RIGHT:
                self.history_pos = self.history_pos + 1
                if self.history_pos > len(self.pms[self.pm_index]._history) - 1:
                    self.history = False
                else:
                    self.pms[self.pm_index].history(self.history_pos)
        else:
            if key != curses.KEY_RIGHT:
                self.history = True
                self.history_pos = len(self.pms[self.pm_index]._history) - 1
                self.pms[self.pm_index].history(self.history_pos)

    def edit_session(self):
        """Edit a session"""
        pass

    def edit_filter(self):
        (max_y, max_x) = self.scr.getmaxyx()
        if self.fullscreen:
            self.ques_pos = max_y - 1
        else:
            self.ques_pos = 3
        key = ""
        self.scr.addstr(self.ques_pos, 0, 'Enter column name : ')
        self.scr.nodelay(0)
        curses.echo()
        self.scr.refresh()
        column = self.scr.getstr()
        if column is not None:
            self.scr.move(self.ques_pos, 0)
            self.scr.clrtoeol()
            txt_value = "Specify a value or regexp [ " + self.pms[self.pm_index].get_filter(column) + " ] : "
            self.scr.addstr(self.ques_pos, 0, 'Specify a value or regexp [ %s ] : ' % (self.pms[self.pm_index].get_filter(column)))
            #scr.move(3, len(txt_value))
            value = self.scr.getstr()
            if value == "":
                value = self.pms[self.pm_index].get_filter(column)
            self.pms[self.pm_index].add_filter(column, value)
            curses.noecho()
            self.scr.nodelay(1)
            self.scr.refresh()
        self.scr.nodelay(1)
        curses.noecho()

    def display_header(self):
        """Display header info"""
        #(max_y, max_x) = self.scr.getmaxyx()
        #if not self.fullscreen:
        #    total_task = 0
        #    filtered_task = 0
        #    if len(self.pms[self.pm_index]._filter) > 0:
        #        total_task = len(self.pms[self.pm_index]._process)
        #        filtered_task = len(self.pms[self.pm_index].process)
        #    else:
        #        total_task = len(self.pms[self.pm_index].process)
        #    if self.pms[self.pm_index].is_online:
        #        status = "Online"
        #    else:
        #        status = "Offline"
        #    self.scr.addstr(0, 0, "Tasks : %s Total, %s filtered, Conn : %d / %d" % (str(total_task), str(filtered_task), self.pm_index + 1, len(self.pms)))
        #    self.scr.addstr(1, 0, 'User : %s, Host : %s, Port : %s, Uptime : %s' % (self.pms[self.pm_index].user[:10], self.pms[self.pm_index].host[:15], self.pms[self.pm_index].port, self.pms[self.pm_index].uptime))
        #    self.scr.addstr(2, 0, 'backend : %s, Version : %s, Status : %s' % (self.pms[self.pm_index].BACKEND, self.pms[self.pm_index].version, status))
        #    if self.pms[self.pm_index].BACKEND == "linux":
        #        self.scr.addstr(4, 0, '%-10s %-11s %-5s %-8s %-5s%s' % ("Pid", "User", "State", "Time", "Info", ' '*(max_x-39)), curses.A_BOLD|curses.A_REVERSE)
        #    elif self.pms[self.pm_index].BACKEND == "Unknown":
        #        self.scr.addstr(4, 0, '%s' % (' '*(max_x)), curses.A_BOLD|curses.A_REVERSE)
        #    else:
        #        self.scr.addstr(4, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s%s' % ('Id', 'User', 'Host', 'Db', 'State', 'Time', 'Info', ' '*(max_x-60)), curses.A_BOLD|curses.A_REVERSE)
        #else:
        #    if self.pms[self.pm_index].BACKEND == "linux":
        #        self.scr.addstr(0, 0, '%-10s %-11s %-5s %-8s %-5s%s' % ("Pid", "User", "State", "Time", "Info", ' '*(max_x-39)), curses.A_BOLD|curses.A_REVERSE)
        #    elif self.pms[self.pm_index].BACKEND == "Unknown":
        #        self.scr.addstr(0, 0, '%s' % (' '*(max_x)), curses.A_BOLD|curses.A_REVERSE)
        #    else:
        #        self.scr.addstr(0, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s%s' % ('Id', 'User', 'Host', 'Db', 'State', 'Time', 'Info', ' '*(max_x-60)), curses.A_BOLD|curses.A_REVERSE)
        #if not self.pms[self.pm_index].is_online and self.pms[self.pm_index].error is not None:
        #    self.scr.addstr(3, 0, 'error : %s' % (self.pms[self.pm_index].error))
        pass

    def display_footer(self):
        """Display footer mainly for action choice from user"""
        (max_y, max_x) = self.scr.getmaxyx()
        text = "[a]dd [c]onnect [d]elay [f]ilter [i]nfo [o]rder [p]aused [r]emove [h]elp [q]uit"
        self.scr.addstr(max_y-1, 0, '%s' % (text).ljust(max_x)[:max_x-1], curses.A_BOLD | curses.A_REVERSE)

    #def move_tops(self):

    def display_tops(self):
        """Display tops to screen"""
        (max_y, max_x) = self.scr.getmaxyx()
        if self.fullscreen:
           cnt = 1
           max_process = max_y - 2
        else:
           cnt = 6
           max_process = max_y - 6

        column = [None] * len(mytop.default_config["drivers"]["mysql"]["process"].keys())
        titles = [None] * len(mytop.default_config["drivers"]["mysql"]["process"].keys())
        for key in mytop.default_config["drivers"]["mysql"]["process"].keys():
            position = mytop.default_config["drivers"]["mysql"]["process"][key]["position"]
            length = mytop.default_config["drivers"]["mysql"]["process"][key]["length"]
            alignment = mytop.default_config["drivers"]["mysql"]["process"][key]["alignment"]
            titles[position] = (mytop.default_config["drivers"]["mysql"]["process"][key]["title"])
            if alignment == "left":
                column[position] = "{: <" + str(length) + "." + str(length) + "}"
            elif alignment == "right":
                column[position] = "{: >" + str(length) + "." + str(length) + "}"
            elif alignment == "center":
                column[position] = "{: ^" + str(length) + "." + str(length) + "}"

        self.scr.addstr(4, 0, " ".join(column).format(*titles).ljust(max_x)[self.cursor_pos_x:max_x], curses.A_BOLD|curses.A_REVERSE)
        for i in self.current_session.history.last():
            informations = [None] * len(mytop.default_config["drivers"]["mysql"]["process"].keys())
            for key in mytop.default_config["drivers"]["mysql"]["process"].keys():
                position = mytop.default_config["drivers"]["mysql"]["process"][key]["position"]
                length = mytop.default_config["drivers"]["mysql"]["process"][key]["length"]
                informations[position] = i[key]
            informations = map(str, informations)
            self.scr.addstr(cnt, 0, " ".join(column).format(*informations)[self.cursor_pos_x:max_x])
            cnt += 1

    def handle_key(self, key):
        if key == ord("a"):
            self.add_session()
        elif key == ord(":"):
            self.command()
        elif key == ord("F"):
            if self.fullscreen:
                self.fullscreen = False
                curses.curs_set(1)
            else:
                self.fullscreen = True
                curses.curs_set(0)
        elif key in [ord("1"), ord("2"), ord("3"), ord("4"), ord("5"), ord("6"), ord("7"), ord("8"), ord("9")]:
           """All keyboard key number are used to select wich connection to display"""
           index = int(chr(key)) - 1
           if index <= len(self.pms) - 1:
               self.pm_index = index
           else:
               self.scr.move(3, 0)
               self.scr.clrtoeol()
               self.scr.addstr(3, 0, "Connection %d does not exist" % (index))
               time.sleep(1)
        elif key == ord("q"):
            """Key to exit mytop"""
            sys.exit(0)
        elif key == ord("h"):
            self.display_help()
        elif key == curses.KEY_LEFT:
            if self.cursor_pos_x > 0:
                self.cursor_pos_x -= 5
        elif key == curses.KEY_RIGHT:
            self.cursor_pos_x += 5
        elif key == ord("d"):
            """Key to change delay"""
            self.edit_delay()
        elif key == ord("e"):
            """Key to edit the current connection"""
            self.edit_pm()
        elif key == ord("f"):
            """key to edit or add filter"""
            self.edit_filter()

        elif key == ord("w"):
            #Key to write results to a file
            write_to_file(scr, pm)
        elif key == curses.KEY_DOWN or key == curses.KEY_UP:
            if key == curses.KEY_DOWN:
                if self.cursor_pos < len(self.pms[self.pm_index].process) - 1:
                    self.cursor_pos = self.cursor_pos + 3
            if key == curses.KEY_UP:
                if self.cursor_pos > 0:
                    self.cursor_pos = self.cursor_pos - 3
            if self.fullscreen:
                self.display_tops()
            else:
                self.display_tops()
            self.scr.move(3, 0)
            self.scr.refresh()
            init_time = time.time()
            while time.time() - init_time < 0.5:
                key = self.scr.getch()
                if key == curses.KEY_DOWN:
                    if self.cursor_pos < len(self.pms[self.pm_index].process) - 1:
                        self.cursor_pos = self.cursor_pos + 1
                elif key == curses.KEY_UP:
                    if self.cursor_pos > 0:
                        self.cursor_pos = self.cursor_pos - 1
                if self.fullscreen:
                    self.display_tops()
                else:
                    self.display_tops()
                self.scr.move(3, 0)
                self.scr.refresh()
        elif key == ord("p"):
            #Key to pause mytop
            if self.paused:
                self.paused = False
                self.delay_counter = self.delay
            else:
                self.paused = True
        elif key == ord("r"):
            #key to remove connection
            self.pms.remove(self.pms[self.pm_index])
            if self.pm_index > len(self.pms) - 1 :
                 self.pm_index = len(self.pms) - 1
            if len(self.pms) == 0:
                 dummy_pm = mytop.create_connection(backend="dummy")
                 self.pms.append(dummy_pm)
                 self.pm_index = 0

    def start(self):
        """Wrappe function if bug and return to display properly"""
        curses.wrapper(self.start_ui)

    def start_ui(self, scr):
        """The main function loop"""
        self.scr = scr #Set screen
        (max_y, max_x) = self.scr.getmaxyx()
        try:
             curses.use_default_colors()
        except curses.error:
             pass
        while 1:
            self.scr.nodelay(1)
            self.scr.keypad(1)
            key = self.scr.getch()
            self.handle_key(key)
            if self.delay_counter  > self.delay:
                self.delay_counter = 0
                self.scr.erase()
                if self.fullscreen:
                    if self.current_session != None:
                        self.display_header()
                        self.display_tops()
                else:
                    if self.current_session != None:
                        self.display_header()
                        self.display_tops()
                    self.display_footer()
                    self.scr.move(3, 0)
            else:
                self.delay_counter = self.delay_counter + 0.1
            curses.napms(100)
            #time.sleep(0.01)
