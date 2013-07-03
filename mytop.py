#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Patrick Charron
# Email : patrick.charron.pc@gmail.com
# Description : MySQL process viewer
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
import curses.textpad
import signal
import getopt
import datetime
import getpass


try: #try to import mytop
    import mytop
except ImportError:
    print "mytop library is missing"
    sys.exit(1)

VERSION = "0.0.2"

def signal_handler(signal, frame):
        sys.exit(1)

def show_usage():
    print """Usage: mytop [OPTION]... -u [USER]...
    """

def show_help():
    print """MySQL process viewer
Example: mytop -u root -h localhost -p password

Options:
  -h, --host=host_name      set hostname
  -p, --password            set password
  -P, --port=port           set port number
  -u, --user=USERNAME       set username

Miscellaneous:
  -V, --version         print version information and exit
  --help                display this help and exit

Behavior:

Report bugs to: patrick.charron.pc@gmail.com"""

def arg_parser():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:P:u:V", ["host=", "password=", "port=", "user=", "version", "help"])
    except getopt.GetoptError, err:
        # print help information and exit:
        show_usage()
        print str(err) # will print something like "option -a not recognized"
        sys.exit(1)
    options = {}
    options["host"] = "localhost"
    options["password"] = None
    options["port"] = 3306
    options["user"] = "root"
    for o, a in opts:
        if o in ("-h", "--host"):
            options["host"] = a
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

    if options["password"] is None:
        options["password"] = getpass.getpass()

    return options

def write_to_file(scr, pm):
    scr.addstr(3, 0, 'Write to : ')
    scr.move(3, 11)
    scr.nodelay(0)
    curses.echo()
    scr.refresh()
    path = scr.getstr()
    if os.path.exists(path) & os.path.isfile(path):
        scr.move(3,0)
        scr.clrtoeol()
        curses.noecho()
        curses.curs_set(0)
        scr.addstr(3, 0, 'File exist. Do you want to overwrite ? [y/N]')
        r = scr.getch()
        if r == ord("y"):
            scr.refresh()
            try :
                f = open(path, "w")
                f.write("Id;User;Host;Db;State;Time;Info\n")
                for p in pm.process:
                    line = str(p.pid) + ";" + p.user + ";" + p.host + ";" + p.db + ";" + p.state + ";" + str(p.time) + ";" + p.info
                    f.write(line + "\n")
                f.close()
            except:
                scr.move(3,0)
                scr.clrtoeol()
                scr.addstr(3, 0, 'Impossible to write file')
                scr.refresh()
                time.sleep(1)
    else:
        try :
            f = open(path, "w")
            f.write("Id;User;Host;Db;State;Time;Info\n")
            for p in pm.process:
                line = str(p.pid) + ";" + p.user + ";" + p.host + ";" + p.db + ";" + p.state + ";" + str(p.time) + ";" + p.info
                f.write(line + "\n")
            f.close()
        except:
            scr.move(3,0)
            scr.clrtoeol()
            scr.addstr(3, 0, 'Impossible to write file')
            scr.refresh()
            time.sleep(1)
    curses.noecho()
    curses.curs_set(1)
    scr.nodelay(1)
    scr.refresh()

def display_filters(scr, pm):
    """
    Display filters to screen
    """
    scr.erase()
    (maxY, maxX) = scr.getmaxyx()
    scr.addstr(0, 0, "Filters")
    scr.addstr(2, 1, "pid", curses.A_BOLD)
    scr.addstr(2, 9, pm.get_filter("pid"))
    scr.addstr(5, 1, "User", curses.A_BOLD)
    scr.addstr(2, 9, pm.get_filter("user"))
    scr.addstr(8, 1, "Host", curses.A_BOLD)
    scr.addstr(2, 9, pm.get_filter("host"))
    scr.addstr(11, 1, "Database", curses.A_BOLD)
    scr.addstr(2, 9, pm.get_filter("database"))
    scr.addstr(14, 1, "State", curses.A_BOLD)
    scr.addstr(2, 9, pm.get_filter("state"))
    scr.addstr(17, 1, "Time", curses.A_BOLD)
    scr.addstr(2, 9, pm.get_filter("time"))
    scr.addstr(20, 1, "Info", curses.A_BOLD)
    scr.addstr(2, 9, pm.get_filter("info"))
    scr.refresh()
    scr.getch()


def display_details(scr, process):
    """
    Display all info about a process
    """
    (maxY, maxX) = scr.getmaxyx()
    scr.erase()
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
    scr.addstr(21, 1, process.info)
    scr.addstr(maxY-1, 0, "Press any key to quit")
    scr.refresh()
    scr.getch()

def display_header(scr, pm):
    """
    Display header info

    """
    (maxY, maxX) = scr.getmaxyx()
    scr.addstr(0, 0, "Tasks : %s Total" % (str(len(pm.process))))
    scr.addstr(1, 0, 'User : %s, Uptime : %s' % (pm.user[:10], pm.uptime))
    scr.addstr(2, 0, 'Version : %s' % (pm.version))
    scr.addstr(4, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s%s' % ('Id', 'User', 'Host', 'Db', 'State', 'Time', 'Info', ' '*(maxX-60)), curses.A_BOLD|curses.A_REVERSE)

def display_footer(scr, text):
    """
    Display footer mainly for action choice from user
    """ 
    (maxY, maxX) = scr.getmaxyx()
    scr.addstr(maxY-1, 0, '%s' % (text), curses.A_BOLD | curses.A_REVERSE)
    scr.hline(maxY-1, len(text), " ", maxX, curses.A_BOLD | curses.A_REVERSE)

def display_process(scr, pm=None, highlight=None):
     """
     Display process to screen
     """
     (maxY, maxX) = scr.getmaxyx()
     cnt = 5
     for p in pm.process[:(maxY-6)]:
         if highlight is not None:
             if highlight == (cnt - 5):
                 scr.addstr(cnt, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s' % (p.pid, p.user[:10], p.host.split(':')[0][:15], p.db[:20], p.state, p.time, p.info[:44]), curses.A_REVERSE)
             else:
                 scr.addstr(cnt, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s' % (p.pid, p.user[:10], p.host.split(':')[0][:15], p.db[:20], p.state, p.time, p.info[:44]))
         else:
             scr.addstr(cnt, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s' % (p.pid, p.user[:10], p.host.split(':')[0][:15], p.db[:20], p.state, p.time, p.info[:44]))
         cnt += 1
#         scr.addstr(cnt, 0, ' '*(maxX-1))

def main(scr, user, db=None):
    """
    This is the main function
    """
    (maxY, maxX) = scr.getmaxyx()
    curses.use_default_colors()
    scr.nodelay(1)
    scr.keypad(1)
    maxInfo = (maxX-75)
    delay_counter = 1
    delay = 1
    paused = False
    cursor_pos = 0
    cursor_max_pos = 0
    while 1:
        key = scr.getch()
        if key == ord("q"):
            sys.exit()
        elif key == ord("h"):
            scr.erase()
            scr.addstr(0, 0, "Help for Interactive Commands")
            scr.addstr(2, 2, "d")
            scr.nodelay(0)
            scr.refresh()
            scr.getch()
            scr.nodelay(1)
        if key == curses.KEY_LEFT:
            scr.addstr(3, 0, 'History', curses.A_BLINK)
            display_process(scr, history[len(history) - 1])
            display_footer(scr, " left right  [q]uit")
            scr.refresh()
            scr.nodelay(0)
            curses.curs_set(0)
        elif key == ord("d"):
            scr.addstr(3, 0, 'Specify delay in second : ')
            scr.move(3, 26)
            scr.nodelay(0)
            curses.echo()
            scr.refresh()
            try:
                delay = int(scr.getstr())
            except:
                scr.move(3,0)
                scr.clrtoeol()
                scr.addstr(3, 0, 'Bad delay value')
                scr.refresh()
                time.sleep(1)
            delay_counter = delay
            curses.noecho()
            scr.nodelay(1)
            scr.refresh()
            scr.erase()
        elif key == ord("f"):
            #display_filters(scr, pm)
            #if len(pm.list_filter()) > 0
            key = ""
            scr.addstr(3, 0, '[p]id [u]ser [h]ost [d]atabase [s]tate [t]ime [i]nfo [r]eset : ')
            scr.move(3, 63)
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
                key = state
            elif key == ord("i"):
                key = "info"
            elif key == ord("r"):
                pm.del_all_filter()
                key = None
            else:
                key = None
            if key is not None:
                scr.move(3,0)
                scr.clrtoeol()
                txt_value = "Specify a value or regexp [ " + pm.get_filter(key) + " ] : "
                scr.addstr(3, 0, 'Specify a value or regexp [ %s ] : ' % (pm.get_filter(key)))
                scr.move(3, len(txt_value))
                value = scr.getstr()
                if value == "":
                    value = pm.get_filter(key)
                pm.add_filter(key, value)
                curses.noecho()
                scr.nodelay(1)
                scr.refresh()
                #scr.erase()
            scr.nodelay(1)
            curses.noecho()
        elif key == ord("k"):
            scr.addstr(3, 0, 'Specify the id process to kill : ')
            scr.move(3, 33)
            scr.nodelay(0)
            curses.echo()
            scr.refresh()
            pids = scr.getstr().split()
            for pid in pids:
                try:
                    db.kill(pid)
                except mytop.processManagerError as e:
                    scr.move(3,0)
                    scr.clrtoeol()
                    scr.addstr(3, 0, '%s' % (e))
                    scr.refresh()
                    time.sleep(1)
            curses.noecho()
            scr.nodelay(1)
            scr.refresh()

        elif key == ord("w"):
            write_to_file(scr, pm)
        elif key == ord("f"):
            scr.addstr(3, 0, 'filter : ')
        elif key == curses.KEY_DOWN:
            if cursor_pos < len(db.process) - 1:
                cursor_pos = cursor_pos + 1
            display_process(scr, db, cursor_pos)
            scr.move(3, 0)
            scr.refresh()
        elif key == curses.KEY_UP:
            if cursor_pos > 0:
                cursor_pos = cursor_pos - 1
            display_process(scr, db, cursor_pos)
            scr.move(3, 0)
            scr.refresh()
        elif key == ord("p"):
            if paused:
                paused = False
                delay_counter = delay
                scr.erase()
            else:
                scr.addstr(3, 0, 'Pause', curses.A_BLINK)
                display_process(scr, db, cursor_pos)
                display_footer(scr, " [u]p  [d]own  [i]nfo  [q]uit")
                scr.refresh()
                paused = True
                scr.nodelay(0)
                curses.curs_set(0)
                while paused:
                    key = scr.getch()
                    if key == curses.KEY_DOWN:
                        if cursor_pos < len(db.process) - 1:
                            cursor_pos = cursor_pos + 1
                        display_process(scr, db, cursor_pos)
                        scr.refresh()
                    elif key == curses.KEY_UP:
                        if cursor_pos > 0:
                            cursor_pos = cursor_pos - 1
                        display_process(scr, db, cursor_pos)
                        scr.refresh()
                    elif key == ord("i"):
                        display_details(scr, db.process[cursor_pos])
                        scr.erase()
                        display_header(scr, db)
                        display_process(scr, db, cursor_pos)
                        display_footer(scr, " [u]p  [d]own  [i]nfo  [q]uit")
                        scr.addstr(3, 0, 'Pause', curses.A_BLINK)
                    elif key == ord("q"):
                        paused = False
                        scr.nodelay(1)
                        curses.curs_set(1)
                        scr.move(3, 0)
                        scr.refresh()
                          
        if delay_counter  > delay and not paused:
            delay_counter = 0                       
            pm.refresh()
            scr.erase()
            display_header(scr, pm)
            display_process(scr, pm, cursor_pos)
            display_footer(scr, " [d]elay  [f]ilter  [H]ighlight  [k]ill  [p]aused  [w]rite  [h]elp  [q]uit")
            scr.move(3, 0)
        else:
            delay_counter = delay_counter + 0.1
        
        time.sleep(0.1)


if __name__ == '__main__':
    #Initialise signal to catch SIGINT
    signal.signal(signal.SIGINT, signal_handler)
    #Call the parser function
    options = arg_parser()
    #Try to connect to the MySQL server
    pm = mytop.processManager(backend="mysql",host=options["host"], user=options["user"], password=options["password"], port=options["port"])
    try:
        pm.connect()
    except mytop.processManagerError as e:
        print "Impossible to connect to the database"
        sys.exit(1)
    #Curses wrapper around the main function
    curses.wrapper(main, options["user"], pm)


