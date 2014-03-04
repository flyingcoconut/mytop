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

import time
import curses
import datetime
import sys

try: #try to import sqltoplib
    import sqltoplib
except ImportError:
    print "sqltoplib library is missing"
    sys.exit(1)

class Ui(object):
    """
    The ui class
    """
    def __init__(self, scr):
        self.fulscreen = False
        self.extension = False
        self.pms = []
        self.pm_index = 0
        #self.maxInfo = (max_x-75)
        self.delay_counter = 1
        self.delay = 1
        self.paused = False
        self.history = False
        self.history_pos = 0
        self.cursor_pos = 0
        self.cursor_max_pos = 0
        self.pm_index = 0
        self.pms = [sqltoplib.create_connection(backend="dummy")]
        self.fullscreen = False
        self.extension = False
        self.scr = scr
        self.formatdb = None


    def write_to_file(self):
        """
        Write process to file in a csv format
        """
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

    def change_delay(self):
        (max_y, max_x) = self.scr.getmaxyx()
        if self.fullscreen:
            ques_pos = max_y - 1
        else:
            ques_pos = 3
        scr.addstr(ques_pos, 0, 'Specify delay in second : ')
        scr.nodelay(0)
        curses.echo()
        scr.refresh()
        try:
            delay = int(scr.getstr())
        except ValueError:
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            scr.addstr(ques_pos, 0, 'Bad delay value')
            scr.refresh()
            time.sleep(1)
            delay = None
        curses.noecho()
        scr.nodelay(1)
        scr.refresh()
        scr.erase()
        return delay

    def ask(self):
        (max_y, max_x) = scr.getmaxyx()
        if fullscreen:
             ques_pos = max_y - 1
        else:
             ques_pos = 3
        scr.nodelay(0)
        curses.echo()
        scr.move(ques_pos, 0)
        scr.clrtoeol()
        scr.addstr(ques_pos, 0, "command : ")
        command = scr.getstr()
        if command == "backend":
            response = "List of disponible backend\n\n"
            for backend in sqltoplib.DISPONIBLE_BACKEND:
                response = response + backend + "\n"
        elif command == "help":
            response = """ List of disponible command\n\n
     backend   List disponible backend
     load      Load connection
     save      save current connection
     help      Display this help
     quit      Quit
    """
            
        elif command == "quit":
            sys.exit(0)
        scr.erase()
        scr.nodelay(0)
        curses.noecho()
        scr.addstr(1, 0, response)
        scr.addstr(max_y - 1, 1, "Press any key to quit")
        scr.getch()
        scr.nodelay(1)
        curses.noecho()

    def add_connection(self):
        """
        Create a new sql connection and return it
        """
        (max_y, max_x) = self.scr.getmaxyx()
        if self.fullscreen:
             ques_pos = max_y - 1
        else:
             ques_pos = 3
        self.scr.nodelay(0)
        curses.echo()
        self.scr.move(ques_pos, 0)
        self.scr.clrtoeol()
        self.scr.addstr(ques_pos, 0, "backend : ")
        value = self.scr.getstr()
        if value != "":
            if value in sqltoplib.DISPONIBLE_BACKEND:
                backend = value
            else:
                self.scr.move(ques_pos, 0)
                self.scr.clrtoeol()
                self.scr.addstr(ques_pos, 0, 'Backend is not valid')
                self.scr.refresh()
                time.sleep(1)
                return None
        if backend == "mysql":
            self.scr.move(ques_pos, 0)
            self.scr.clrtoeol()
            self.scr.addstr(ques_pos, 0, "host [localhost] : ")
            value = self.scr.getstr()
            if value is "":
                host = "localhost"
            else:
                host = value
            self.scr.move(ques_pos, 0)
            self.scr.clrtoeol()
            self.scr.addstr(ques_pos, 0, "user [root] : ")
            value = self.scr.getstr()
            if value is "":
                user = "root"
            else:
                user = value
            self.scr.move(ques_pos, 0)
            self.scr.clrtoeol()
            self.scr.addstr(ques_pos, 0, "port [3306] : ")
            value = self.scr.getstr()
            if value is "":
                port  = 3306
            else:
                port = int(value)
            self.scr.move(ques_pos, 0)
            self.scr.clrtoeol()
            curses.noecho()
            self.scr.addstr(ques_pos, 0, "password : ")
            value = self.scr.getstr()
            password = value
            new_pm = sqltoplib.create_connection(backend=backend, host=host, user=user, port=port, password=password)
        elif backend == "redisdb":
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            scr.addstr(ques_pos, 0, "host [localhost] : ")
            value = scr.getstr()
            if value is "":
                host = "localhost"
            else:
                host = value
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            scr.addstr(ques_pos, 0, "port [6379] : ")
            value = scr.getstr()
            if value is "":
                port  = 6379
            else:
                port = int(value)
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            curses.noecho()
            scr.addstr(ques_pos, 0, "password : ")
            value = scr.getstr()
            password = value
            new_pm = sqltoplib.create_connection(backend=backend, host=host, port=port, password=password)
        elif backend == "linux":
            new_pm = sqltoplib.create_connection(backend=backend)
        else:
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            scr.addstr(ques_pos, 0, "host [localhost] : ")
            value = scr.getstr()
            if value is "":
                host = "localhost"
            else:
                host = value
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            scr.addstr(ques_pos, 0, "user : ")
            value = scr.getstr()
            user = value
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            scr.addstr(ques_pos, 0, "port : ")
            value = scr.getstr()
            port = int(value)
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            curses.noecho()
            scr.addstr(ques_pos, 0, "password : ")
            value = scr.getstr()
            password = value
            new_pm = sqltoplib.create_connection(backend=backend, host=host, user=user, port=port, password=password)
        try:
            new_pm.connect()
        except sqltoplib.processmanager.ProcessManagerError:
            pass
        if new_pm is not None:
            if self.pms[self.pm_index].BACKEND == "Unknown":
                self.pms.remove(self.pms[self.pm_index])
            self.pms.append(new_pm)
            self.pm_index = len(self.pms) - 1
        self.scr.nodelay(1)
        curses.noecho()

    def help(self):
        """
        Display help
        """
        help_text = """
     Keyboard shortcut
     
     [a]dd          Add a new connection
     [c]onnect      Connect or disconnect
     [d]elay        Modify delay between refresh
     [e]dit         Edit current connection
     [E]xtension    Display extended functionality  
     [f]ilter       Filter process
     [F]ullscreen   Display in fullscreen mode
     [i]nfo         Get complete info on process
     [o]rder        Order process
     [p]aused       Pause
     [r]emove       Remove current connection
     [s]tats        Get complete stats about current connection
     [w]rite        Dump process to a csv file
     [h]elp         Display this help 
     [q]uit         Quit
     [:]            Interactive command
     
     Use up and down arrow to select process
     Use left and right arrow to navigate history
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

    def edit_connection(self):
        """
        Edit a sql conection
        """
        reload_pm = False
        scr.nodelay(0)
        curses.echo()
        scr.move(3, 0)
        scr.clrtoeol()
        scr.addstr(3, 0, "host [ %s ] : " % (pm.host))
        value = scr.getstr()
        if value != "":
            pm.host = value
            reload_pm = True
        scr.move(3, 0)
        scr.clrtoeol()
        scr.addstr(3, 0, "user [ %s ] : " % (pm.user))
        value = scr.getstr()
        if value != "":
            pm.user = value
            reload_pm = True
        scr.move(3, 0)
        scr.clrtoeol()
        scr.addstr(3, 0, "port [ %s ] : " % (pm.port))
        value = scr.getstr()
        if value != "":
            pm.port = int(value)
            reload_pm = True
        scr.move(3, 0)
        scr.clrtoeol()
        curses.noecho()
        scr.addstr(3, 0, "password : ")
        value = scr.getstr()
        if value != "":
            pm.password = value
            reload_pm = True

        if reload_pm:
            pm.close()
            try:
                pm.connect()
            except:
                pass
        scr.nodelay(1)
        curses.noecho()

    def display_details(self):
        """
        Display all info about a process
        """
        (max_y, max_x) = scr.getmaxyx()
        scr.erase()
        scr.nodelay(0)
        curses.curs_set(0)
        scr.addstr(0, 0, "Process infos")
        scr.addstr(2, 1, "Id", curses.A_BOLD)
        scr.addstr(3, 1, str(process.pid))
        scr.addstr(5, 1, "User", curses.A_BOLD)
        scr.addstr(6, 1, process.user)
        scr.addstr(8, 1, "Host", curses.A_BOLD)
        scr.addstr(9, 1, process.host)
        scr.addstr(11, 1, "Database", curses.A_BOLD)
        scr.addstr(12, 1, process.db)
        scr.addstr(14, 1, "State", curses.A_BOLD)
        scr.addstr(15, 1, process.state)
        scr.addstr(17, 1, "Time", curses.A_BOLD)
        scr.addstr(18, 1, str(datetime.timedelta(seconds=process.time)))
        scr.addstr(20, 1, "Info", curses.A_BOLD)
        info = process.info
        try:
            scr.addstr(22, 0, info)
        except _curses.error:
            scr.addstr(22, 0, "Sql request is too long to display")
        scr.addstr(max_y-1, 0, "Press any key to quit")
        scr.refresh()
        scr.getch()
        scr.nodelay(1)
        curses.curs_set(1)

    def add_filter(self):
        (max_y, max_x) = scr.getmaxyx()
        if self.fullscreen:
            ques_pos = max_y - 1
        else:
            ques_pos = 3
        key = ""
        scr.addstr(ques_pos, 0, '[p]id [u]ser [h]ost [d]atabase [s]tate [t]ime [i]nfo [r]eset : ')
        scr.nodelay(0)
        curses.echo()
        scr.refresh()
        key = scr.getch()
        if key == ord("p"):
            key = "pid"
        elif key == ord("u"):
            key = "user"
        elif key == ord("h"):
            key = "host"
        elif key == ord("d"):
            key = "db"
        elif key == ord("s"):
            key = "state"
        elif key == ord("t"):
            key = "time"
        elif key == ord("i"):
            key = "info"
        elif key == ord("r"):
            pm.del_all_filter()
            key = None
        else:
            key = None
        if key is not None:
            scr.move(ques_pos, 0)
            scr.clrtoeol()
            txt_value = "Specify a value or regexp [ " + pm.get_filter(key) + " ] : "
            scr.addstr(ques_pos, 0, 'Specify a value or regexp [ %s ] : ' % (pm.get_filter(key)))
            #scr.move(3, len(txt_value))
            value = scr.getstr()
            if value == "":
                value = pm.get_filter(key)
            pm.add_filter(key, value)
            curses.noecho()
            scr.nodelay(1)
            scr.refresh()
        scr.nodelay(1)
        curses.noecho()

    def display_header(self):
        """
        Display header info

        """
        (max_y, max_x) = self.scr.getmaxyx()
        if not self.fullscreen:
            total_task = 0
            filtered_task = 0
            if len(self.pms[self.pm_index]._filter) > 0:
                total_task = len(self.pms[self.pm_index]._process)
                filtered_task = len(self.pms[self.pm_index].process)
            else:
                total_task = len(self.pms[self.pm_index].process)
            if self.pms[self.pm_index].is_online:
                status = "Online"
            else:
                status = "Offline"
            self.scr.addstr(0, 0, "Tasks : %s Total, %s filtered, Conn : %d / %d" % (str(total_task), str(filtered_task), self.pm_index + 1, len(self.pms)))
            self.scr.addstr(1, 0, 'User : %s, Host : %s, Port : %s, Uptime : %s' % (self.pms[self.pm_index].user[:10], self.pms[self.pm_index].host[:15], self.pms[self.pm_index].port, self.pms[self.pm_index].uptime))
            self.scr.addstr(2, 0, 'backend : %s, Version : %s, Status : %s' % (self.pms[self.pm_index].BACKEND, self.pms[self.pm_index].version, status))
            if self.pms[self.pm_index].BACKEND == "linux":
                self.scr.addstr(4, 0, '%-10s %-11s %-5s %-8s %-5s%s' % ("Pid", "User", "State", "Time", "Info", ' '*(max_x-39)), curses.A_BOLD|curses.A_REVERSE)
            elif self.pms[self.pm_index].BACKEND == "Unknown":
                self.scr.addstr(4, 0, '%s' % (' '*(max_x)), curses.A_BOLD|curses.A_REVERSE)
            else:
                self.scr.addstr(4, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s%s' % ('Id', 'User', 'Host', 'Db', 'State', 'Time', 'Info', ' '*(max_x-60)), curses.A_BOLD|curses.A_REVERSE)
        else:
            if self.pms[self.pm_index].BACKEND == "linux":
                self.scr.addstr(0, 0, '%-10s %-11s %-5s %-8s %-5s%s' % ("Pid", "User", "State", "Time", "Info", ' '*(max_x-39)), curses.A_BOLD|curses.A_REVERSE)
            elif self.pms[self.pm_index].BACKEND == "Unknown":
                self.scr.addstr(0, 0, '%s' % (' '*(max_x)), curses.A_BOLD|curses.A_REVERSE)
            else:
                self.scr.addstr(0, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s%s' % ('Id', 'User', 'Host', 'Db', 'State', 'Time', 'Info', ' '*(max_x-60)), curses.A_BOLD|curses.A_REVERSE)
        if not self.pms[self.pm_index].is_online and self.pms[self.pm_index].error is not None:
            self.scr.addstr(3, 0, 'error : %s' % (pm.error))

    def display_footer(self, text):
        """
        Display footer mainly for action choice from user
        """ 
        (max_y, max_x) = self.scr.getmaxyx()
        self.scr.addstr(max_y-1, 0, '%s' % (text), curses.A_BOLD | curses.A_REVERSE)
        self.scr.hline(max_y-1, len(text), " ", max_x, curses.A_BOLD | curses.A_REVERSE)

    def display_process(self):
        """
        Display process to screen
        """
        (max_y, max_x) = self.scr.getmaxyx()
        if self.fullscreen:
           cnt = 1
           max_process = max_y - 2
        else:
           cnt = 5
           max_process = max_y-6
        highlight = self.cursor_pos
        if highlight > len(self.pms[self.pm_index].process):
            highlight = len(self.pms[self.pm_index].process) - 1
        for process in self.pms[self.pm_index].process[:(max_process)]:
            if highlight is not None:
                if highlight == (cnt - 5):
                    if self.pms[self.pm_index].BACKEND == "linux":
                        self.scr.addstr(cnt, 0, '%-10s %-11s %-5s %-8s %-5s' % (process["pid"], process["user"][:10], process["state"], process["time"], process["info"][:44]), curses.A_REVERSE)
                    elif self.pms[self.pm_index].BACKEND == "redisdb":
                        self.scr.addstr(cnt, 0, '%-11s %-5s %-8s %-5s' % (process.user, process.state, process.time, process.info[:44]), curses.A_REVERSE)
                    elif self.pms[self.pm_index].BACKEND == "mysql":
                        self.scr.addstr(cnt, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s' % (process["pid"], process["user"][:10], process["host"].split(':')[0][:15], process["db"][:20], process["state"], process["time"], process["info"][:44]), curses.A_REVERSE)
                    else:
                        self.scr.addstr(cnt, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s' % (process.pid, process.user[:10], process.host.split(':')[0][:15], process.db[:20], process.state, process.time, process.info[:44]), curses.A_REVERSE)
                else:
                    if self.pms[self.pm_index].BACKEND == "linux":
                        self.scr.addstr(cnt, 0, '%-10s %-11s %-5s %-8s %-5s' % (process["pid"], process["user"][:10], process["state"], process["time"], process["info"][:44]))
                    elif self.pms[self.pm_index].BACKEND == "redisdb":
                        self.scr.addstr(cnt, 0, '%-11s %-5s %-8s %-5s' % (process.user, process.state, process.time, process.info[:44]))
                    elif self.pms[self.pm_index].BACKEND == "mysql":
                        self.scr.addstr(cnt, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s' % (process["pid"], process["user"][:10], process["host"].split(':')[0][:15], process["db"][:20], process["state"], process["time"], process["info"][:44]))
                    else:
                        self.scr.addstr(cnt, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s' % (process.pid, process.user[:10], process.host.split(':')[0][:15], process.db[:20], process.state, process.time, process.info[:44]))
            else:
                if self.pms[self.pm_index].BACKEND == "linux":
                    self.scr.addstr(cnt, 0, '%-10s %-11s %-5s %-8s %-5s' % (process["pid"], process["user"][:10], process["state"], process["time"], process["info"][:44]))
                elif self.pms[self.pm_index].BACKEND == "redisdb":
                    self.scr.addstr(cnt, 0, '%-11s %-5s %-8s %-5s' % (process.user, process.state, process.time, process.info[:44]))
                else:
                    self.scr.addstr(cnt, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s' % (process.pid, process.user[:10], process.host.split(':')[0][:15], process.db[:20], process.state, process.time, process.info[:44]))
            cnt += 1



    def start_ui(self):
        """
        The main function
        """
        (max_y, max_x) = self.scr.getmaxyx()
        try:
             curses.use_default_colors()
        except curses.error:
             pass
        self.scr.nodelay(1)
        self.scr.keypad(1)
        while 1:
            key = self.scr.getch()
            if key == ord("a"):
                #Key for adding a sql connection
                self.add_connection()
            elif key == ord("c"):
                if self.pms[self.pm_index].is_online:
                    self.pms[self.pm_index].disconnect()
                else:
                    try:
                        self.pms[self.pm_index].connect()
                    except:
                        pass
            elif key == ord(":"):
                ask(scr, fullscreen=fullscreen)
            elif key == ord("F"):
                if self.fullscreen:
                    self.fullscreen = False
                    curses.curs_set(1)
                else:
                    self.fullscreen = True
                    curses.curs_set(0)
            elif key in [ord("1"), ord("2"), ord("3"), ord("4"), ord("5"), ord("6"), ord("7"), ord("8"), ord("9")]:
               #All keyboard key number are used to select wich connection to display
               index = int(chr(key)) - 1
               if index <= len(pms) - 1:
                   pm_index = index
               else:
                   scr.move(3, 0)
                   scr.clrtoeol()
                   scr.addstr(3, 0, "Connection %d does not exist" % (index))
                   time.sleep(1)
            elif key == ord("q"):
                #Key to exit mytop
                sys.exit(0)
            elif key == ord("h"):
                self.help()
            elif key == curses.KEY_LEFT or key == curses.KEY_RIGHT:
                #Key to navigate history
                if len(pms[pm_index]._history) == 0:
                    scr.addstr(3, 0, 'No history')
                    time.sleep(1)
                elif history:
                    if key == curses.KEY_LEFT:
                        if history_pos != 0:
                            history_pos = history_pos - 1
                            pms[pm_index].history(history_pos)
                    if key == curses.KEY_RIGHT:
                        history_pos = history_pos + 1
                        if history_pos > len(pm._history) - 1:
                            history = False
                        else:
                            pm.history(history_pos)
                else:
                    if key != curses.KEY_RIGHT:
                        history = True
                        history_pos = len(pms[pm_index]._history) - 1
                        pms[pm_index].history(history_pos)
            elif key == ord("d"):
                #Key to change delay
                changed_delay = change_delay(scr, fullscreen=fullscreen)
                if changed_delay is not None:
                    delay_counter = changed_delay
                    delay = changed_delay
                
            elif key == ord("e"):
                #Key to edit the current connection
                edit_connection(scr, pm)
            elif key == ord("f"):
                #key to edit or add filter
                add_filter(scr, pms[pm_index], fullscreen=fullscreen)
            elif key == ord("k"):
                #key to kill sql process to threads
                scr.addstr(3, 0, 'Specify the id process to kill : ')
                scr.move(3, 33)
                scr.nodelay(0)
                curses.echo()
                scr.refresh()
                pids = scr.getstr().split()
                for pid in pids:
                    try:
                        pm.kill(pid)
                    except sqltoplib.processManagerError:
                        scr.move(3, 0)
                        scr.clrtoeol()
                        scr.addstr(3, 0, '%s' % (e))
                        scr.refresh()
                        time.sleep(1)
                curses.noecho()
                scr.nodelay(1)
                scr.refresh()

            elif key == ord("w"):
                #Key to write results to a file
                write_to_file(scr, pm)
            elif key == curses.KEY_DOWN or key == curses.KEY_UP:
                if key == curses.KEY_DOWN:
                    if self.cursor_pos < len(self.pms[self.pm_index].process) - 1:
                        self.cursor_pos = self.cursor_pos + 1
                if key == curses.KEY_UP:
                    if self.cursor_pos > 0:
                        self.cursor_pos = self.cursor_pos - 1
                if self.fullscreen:
                    self.display_process()
                else:
                    self.display_process()
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
                        self.display_process()
                    else:
                        self.display_process()
                    self.scr.move(3, 0)
                    self.scr.refresh()
            elif key == ord("i"):
                #Key to display details about a process
                display_details(scr, pms[pm_index].process[cursor_pos])
                scr.erase()
            elif key == ord("p"):
                #Key to pause mytop
                if paused:
                    paused = False
                    delay_counter = delay
                else:
                    paused = True
            elif key == ord("r"):
                #key to remove connection
                pms.remove(pms[pm_index]) 
                if pm_index > len(pms) - 1 :
                     pm_index = len(pms) - 1
                if len(pms) == 0:
                     dummy_pm = sqltoplib.create_connection(backend="dummy")
                     pms.append(dummy_pm)
                     pm_index = 0
            if self.delay_counter  > self.delay:
                self.delay_counter = 0
                for p in self.pms: 
                    try:
                        if p.is_online:         
                            p.refresh()
                    except sqltoplib.processmanager.ProcessManagerError:
                        pass
            elif self.paused:
                pass
            elif self.history:
                pass
            else:
                self.delay_counter = self.delay_counter + 0.1
            
            self.scr.erase()
            if self.fullscreen:
                self.display_header()
                self.display_process()
            else:
                pass
                self.display_header()
                self.display_process()
                self.display_footer("[a]dd [c]onnect [d]elay [f]ilter [i]nfo [o]rder [p]aused [r]emove [h]elp [q]uit")
                self.scr.move(3, 0)
            #curses.curs_set(1)
            if self.paused or self.history:
                curses.curs_set(0)
                self.scr.addstr(3, 0, 'Pause', curses.A_BLINK)
            if self.history:
                curses.curs_set(0)
                self.scr.addstr(3, 0, 'History (%s / %s)' % (str(history_pos), str(len(pm._history) - 1)), curses.A_BLINK)
            time.sleep(0.1)
