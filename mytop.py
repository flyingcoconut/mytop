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

import os
import sys
import time
import curses
import signal
import getopt
import datetime
import getpass


try: #try to import sqltoplib
    import sqltoplib
except ImportError:
    print "sqltoplib library is missing"
    sys.exit(1)

try:
    import sqlparse
except ImportError:
    pass

VERSION = "0.0.2"

def signal_handler(sig, frame):
    """
    Get signals and exit
    """
    sys.exit(1)

def show_usage():
    """
    Print a usage message
    """
    print """Usage: mytop [OPTION]... -u [USER]...
    """

def show_help():
    """Print a help message"""
    print """MySQL process viewer
Example: mytop -u root -h localhost -p password

Options:
  -b, --backend=BACKEND     set the backend (mysql, mongodb, pgsql)
  -h, --host=HOSTNAME       set hostname
  -l, --list                list all backend
  -p, --password=PASSWORD   set password
  -P, --port=PORT           set port number
  -u, --user=USERNAME       set username

Miscellaneous:
  -V, --version         print version information and exit
  --help                display this help and exit

Report bugs to: patrick.charron.pc@gmail.com"""

def arg_parser():
    """
    Function to parse command line arguments
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "b:h:lp:P:u:V", ["backend=", "host=", "list", "password=", "port=", "user=", "version", "help"])
    except getopt.GetoptError, err:
        # print help information and exit:
        show_usage()
        print str(err) # will print something like "option -a not recognized"
        sys.exit(1)
    options = {}
    options["host"] = "localhost"
    options["password"] = None
    options["port"] = 0
    options["user"] = None
    options["backend"] = None
    for o, a in opts:
        if o in ("-b", "--backend"):
            options["backend"] = a
        elif o in ("-h", "--host"):
            options["host"] = a
        elif o in ("-l", "--list"):
            for backend in sqltoplib.DISPONIBLE_BACKEND:
                print backend
            sys.exit(0)
        elif o in ("-p", "--password"):
            options["password"] = a
        elif o in ("-P", "--port"):
            options["port"] = int(a)
        elif o in ("-u", "--user"):
            options["user"] = a
        elif o in ("-V", "--version"):
            print "Version %s" % VERSION
            sys.exit(0)
        elif o == "--help":
            show_usage()
            show_help()
            sys.exit(0)
        else:
            show_usage()
            sys.exit(1)
    if options["backend"] is None:
        print "no type specified"
        sys.exit(1)
    if options["backend"] not in sqltoplib.DISPONIBLE_BACKEND:
        print "is not a valid type"
        sys.exit(1)
    return options

def write_to_file(scr, pm):
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

def add_connection(scr):
    """
    Create a new sql connection and return it
    """
    scr.nodelay(0)
    curses.echo()
    scr.move(3, 0)
    scr.clrtoeol()
    scr.addstr(3, 0, "backend : ")
    value = scr.getstr()
    if value != "":
        if value in sqltoplib.DISPONIBLE_BACKEND:
            backend = value
        else:
            scr.move(3, 0)
            scr.clrtoeol()
            scr.addstr(3, 0, 'Backend is not valid')
            scr.refresh()
            time.sleep(1)
            return None
    new_pm = sqltoplib.create_connection(backend=backend)
    scr.move(3, 0)
    scr.clrtoeol()
    scr.addstr(3, 0, "host : ")
    value = scr.getstr()
    if value != "":
        new_pm.host = value
    scr.move(3, 0)
    scr.clrtoeol()
    scr.addstr(3, 0, "user : ")
    value = scr.getstr()
    if value != "":
        new_pm.user = value
    scr.move(3, 0)
    scr.clrtoeol()
    scr.addstr(3, 0, "port : ")
    value = scr.getstr()
    if value != "":
        new_pm.port = int(value)
    scr.move(3, 0)
    scr.clrtoeol()
    curses.noecho()
    scr.addstr(3, 0, "password : ")
    value = scr.getstr()
    if value != "":
        new_pm.password = value
    try:
        new_pm.connect()
    except sqltoplib.ProcessManagerError:
        pass
    scr.nodelay(1)
    curses.noecho()
    return new_pm

def edit_connection(scr, pm):
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



def display_details(scr, process):
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
    try:
        info = sqlparse.format(process.info, reindent=True, keyword_case = "upper")
    except:
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

def display_header(scr, pm, index, pms):
    """
    Display header info

    """
    (max_y, max_x) = scr.getmaxyx()
    total_task = 0
    filtered_task = 0
    if len(pm._filter) > 0:
        total_task = len(pm._process)
        filtered_task = len(pm.process)
    else:
        total_task = len(pm.process)
    scr.addstr(0, 0, "Tasks : %s Total, %s filtered, Conn : %d / %d" % (str(total_task), str(filtered_task), index + 1, len(pms)))
    scr.addstr(1, 0, 'User : %s, Host : %s, Port : %s, Uptime : %s' % (pm.user[:10], pm.host[:15], pm.port, pm.uptime))
    scr.addstr(2, 0, 'backend : %s, Version : %s' % (pm.BACKEND, pm.version))
    scr.addstr(4, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s%s' % ('Id', 'User', 'Host', 'Db', 'State', 'Time', 'Info', ' '*(max_x-60)), curses.A_BOLD|curses.A_REVERSE)

def display_footer(scr, text, text2):
    """
    Display footer mainly for action choice from user
    """ 
    (max_y, max_x) = scr.getmaxyx()
    scr.addstr(max_y-2, 0, '%s' % (text), curses.A_BOLD | curses.A_REVERSE)
    scr.hline(max_y-2, len(text), " ", max_x, curses.A_BOLD | curses.A_REVERSE)
    scr.addstr(max_y-1, 0, '%s' % (text2), curses.A_BOLD | curses.A_REVERSE)
    scr.hline(max_y-1, len(text2), " ", max_x, curses.A_BOLD | curses.A_REVERSE)

def display_process(scr, pm=None, highlight=None):
    """
    Display process to screen
    """
    (max_y, max_x) = scr.getmaxyx()
    cnt = 5
    if highlight > len(pm.process):
        highlight = len(pm.process) - 1
    for process in pm.process[:(max_y-6)]:
        if highlight is not None:
            if highlight == (cnt - 5):
                scr.addstr(cnt, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s' % (process.pid, process.user[:10], process.host.split(':')[0][:15], process.db[:20], process.state, process.time, process.info[:44]), curses.A_REVERSE)
            else:
                scr.addstr(cnt, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s' % (process.pid, process.user[:10], process.host.split(':')[0][:15], process.db[:20], process.state, process.time, process.info[:44]))
        else:
            scr.addstr(cnt, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s' % (process.pid, process.user[:10], process.host.split(':')[0][:15], process.db[:20], process.state, process.time, process.info[:44]))
        cnt += 1

def main(scr, pm=None):
    """
    The main function
    """
    (max_y, max_x) = scr.getmaxyx()
    curses.use_default_colors()
    scr.nodelay(1)
    scr.keypad(1)
    maxInfo = (max_x-75)
    delay_counter = 1
    delay = 1
    paused = False
    history = False
    history_pos = 0
    cursor_pos = 0
    cursor_max_pos = 0
    pm_index = 0
    pms = []
    pms.append(pm)
    config = sqltoplib.Config(".mytop.conf")
    config.parse()
    pm.max_history = int(config.get_config("max_history"))
    
    while 1:
        key = scr.getch()
        if key == ord("a"):
            #Key for adding a sql connection
            new_pm = add_connection(scr)
            pms.append(new_pm)
        if key in [ord("1"), ord("2"), ord("3"), ord("4"), ord("5"), ord("6"), ord("7"), ord("8"), ord("9")]:
           #All keyboard key number are used to select wich connection to display
           index = int(chr(key)) - 1
           if index <= len(pms) - 1:
               pm_index = index
           else:
               scr.move(3, 0)
               scr.clrtoeol()
               scr.addstr(3, 0, "Connection %d does not exist" % (index))
               time.sleep(1)
        if key == ord("q"):
            #Key to exit mytop
            sys.exit(0)
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
            scr.addstr(3, 0, 'Specify delay in second : ')
            scr.move(3, 26)
            scr.nodelay(0)
            curses.echo()
            scr.refresh()
            try:
                delay = int(scr.getstr())
            except ValueError:
                scr.move(3, 0)
                scr.clrtoeol()
                scr.addstr(3, 0, 'Bad delay value')
                scr.refresh()
                time.sleep(1)
            delay_counter = delay
            curses.noecho()
            scr.nodelay(1)
            scr.refresh()
            scr.erase()
        elif key == ord("e"):
            #Key to edit the current connection
            edit_connection(scr, pm)
        elif key == ord("f"):
            #key to edit or add filter
            key = ""
            scr.addstr(3, 0, '[p]id [u]ser [h]ost [d]atabase [s]tate [t]ime [i]nfo [r]eset : ')
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
                pms[pm_index].del_all_filter()
                key = None
            else:
                key = None
            if key is not None:
                scr.move(3, 0)
                scr.clrtoeol()
                txt_value = "Specify a value or regexp [ " + pms[pm_index].get_filter(key) + " ] : "
                scr.addstr(3, 0, 'Specify a value or regexp [ %s ] : ' % (pms[pm_index].get_filter(key)))
                scr.move(3, len(txt_value))
                value = scr.getstr()
                if value == "":
                    value = pms[pm_index].get_filter(key)
                pms[pm_index].add_filter(key, value)
                curses.noecho()
                scr.nodelay(1)
                scr.refresh()
            scr.nodelay(1)
            curses.noecho()
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
                if cursor_pos < len(pms[pm_index].process) - 1:
                    cursor_pos = cursor_pos + 1
            if key == curses.KEY_UP:
                if cursor_pos > 0:
                    cursor_pos = cursor_pos - 1
            display_process(scr, pms[pm_index], cursor_pos)
            scr.move(3, 0)
            scr.refresh()
            init_time = time.time()
            while time.time() - init_time < 0.5:
                key = scr.getch()
                if key == curses.KEY_DOWN:
                    if cursor_pos < len(pms[pm_index].process) - 1:
                        cursor_pos = cursor_pos + 1
                elif key == curses.KEY_UP:
                    if cursor_pos > 0:
                        cursor_pos = cursor_pos - 1
                display_process(scr, pms[pm_index], cursor_pos)
                scr.move(3, 0)
                scr.refresh()
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
                scr.nodelay(0)
                curses.echo()
                scr.move(3, 0)
                scr.clrtoeol()
                scr.addstr(3, 0, "Specify the connection to remove : ")
                try:
                    value = int(scr.getstr())
                except ValueError:
                    scr.move(3, 0)
                    scr.clrtoeol()
                    scr.addstr(3, 0, "Connection must be a number")
                    time.sleep(1)
                else:
                    try:
                        pms.pop(value - 1)
                    except KeyError:
                        scr.move(3, 0)
                        scr.clrtoeol()
                        scr.addstr(3, 0, "Connection %s does not exist" % (value))
                                            
        if delay_counter  > delay:
            delay_counter = 0
            for p in pms: 
                try:                 
                    p.refresh()
                except sqltoplib.processmanager.ProcessManagerError:
                    pass
        elif paused:
            pass
        elif history:
            pass
        else:
            delay_counter = delay_counter + 0.1
        
        scr.erase()
        display_header(scr, pms[pm_index], pm_index, pms)
        display_process(scr, pms[pm_index], cursor_pos)
        display_footer(scr, "[a]dd  [d]elay  [e]dit  [f]ilter  [F]ullscreen  [i]nfo  [k]ill  [o]rder  [p]aused", "[r]emove  [s]ats  [w]rite  [q]uit")
        scr.move(3, 0)
        curses.curs_set(1)
        if paused or history:
            curses.curs_set(0)
            scr.addstr(3, 0, 'Pause', curses.A_BLINK)
        if history:
            curses.curs_set(0)
            scr.addstr(3, 0, 'History (%s / %s)' % (str(history_pos), str(len(pm._history) - 1)), curses.A_BLINK)
        time.sleep(0.1)


if __name__ == '__main__':
    #Initialise signal to catch SIGINT
    signal.signal(signal.SIGINT, signal_handler)
    #Call the parser function
    args = arg_parser()
    #Try to connect to the MySQL server
    if args["type"] == "mysql":
        pm = sqltoplib.mysql.ProcessManager(host=args["host"], user=args["user"], password=args["password"], port=args["port"])
    elif args["type"] == "mongodb":
        pm = sqltoplib.mongodb.ProcessManager(host=args["host"], user=args["user"], password=args["password"], port=args["port"])
    elif args["type"] == "redisdb":
        pm = sqltoplib.redisdb.ProcessManager(host=args["host"], user=args["user"], password=args["password"], port=args["port"])
    try:
        pm.connect()
    except sqltoplib.processmanager.ProcessManagerError:
        pass
    #Curses wrapper around the main function
    curses.wrapper(main, pm)


