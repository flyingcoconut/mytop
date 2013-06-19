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
#
#
# Things to do
#
# add kill feature in paused mode
# add explain feature for sql query
# add filter function
# add more resizing capabilities
# add highlight capabilities with colors
# add a preference (config file) eg. .mytop.conf in home
# add a better help
# add a better scrolling during pause for process
# add write to file capabilties
# add a background thread for mysql processing and query
# mysql serveur aggregation

import os
import sys
import time
import curses
import signal
import getopt
import datetime
import getpass

# 3rd Party imports
import MySQLdb


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
            print "Version"
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

def display_details(scr, process):
    (maxY, maxX) = scr.getmaxyx()
    scr.erase()
    scr.addstr(0, 0, "Process infos")
    scr.addstr(2, 1, "Id", curses.A_BOLD)
    scr.addstr(3, 1, str(process[0]))
    scr.addstr(5, 1, "User", curses.A_BOLD)
    scr.addstr(6, 1, process[1])
    scr.addstr(8, 1, "Host", curses.A_BOLD)
    scr.addstr(9, 1, process[2])
    scr.addstr(11, 1, "Database", curses.A_BOLD)
    scr.addstr(12, 1, process[3])
    scr.addstr(14, 1, "State", curses.A_BOLD)
    scr.addstr(15, 1, process[4])
    scr.addstr(17, 1, "Time", curses.A_BOLD)
    scr.addstr(18, 1, str(datetime.timedelta(seconds=process[5])))
    scr.addstr(20, 1, "Info", curses.A_BOLD)
    scr.addstr(21, 1, process[6])
    scr.addstr(maxY-1, 0, "Press any key to quit")
    scr.refresh()
    scr.getch()

def display_header(scr, info):
    (maxY, maxX) = scr.getmaxyx()
    scr.addstr(0, 0, time.ctime())
    scr.addstr(1, 0, 'User : %s, Uptime : %s' % (info["user"][:10], info["uptime"]))
    scr.addstr(2, 0, 'Version : %s' % (info["version"]))
    scr.addstr(4, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s%s' % ('Id', 'User', 'Host', 'Db', 'State', 'Time', 'Info', ' '*(maxX-60)), curses.A_BOLD|curses.A_REVERSE)

def display_footer(scr, text): 
    (maxY, maxX) = scr.getmaxyx()
    text = text.ljust(maxX-1)
    scr.addstr(maxY-1, 0, '%s' % (text), curses.A_BOLD | curses.A_REVERSE)

def display_process(scr, process=None, highlight=None):
     (maxY, maxX) = scr.getmaxyx()
     cnt = 5
     for p in process[:(maxY-6)]:
         if highlight is not None:
             if highlight == (cnt - 5):
                 scr.addstr(cnt, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s' % (p[0], p[1][:10], p[2].split(':')[0][:15], p[3][:20], p[4], p[5], p[6]), curses.A_REVERSE)
             else:
                 scr.addstr(cnt, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s' % (p[0], p[1][:10], p[2].split(':')[0][:15], p[3][:20], p[4], p[5], p[6]))
         else:
             scr.addstr(cnt, 0, '%-10s %-11s %-15s %-20s %-5s %-8s %-5s' % (p[0], p[1][:10], p[2].split(':')[0][:15], p[3][:20], p[4], p[5], p[6]))
         cnt += 1
#         scr.addstr(cnt, 0, ' '*(maxX-1))

def getStats(scr, user, db=None):
    (maxY, maxX) = scr.getmaxyx()
    curses.use_default_colors()
    scr.nodelay(1)
    scr.keypad(1)
    sql = db.cursor()
    fp = open('debug', 'w+')
    maxInfo = (maxX-75)
    delay_counter = 1
    delay = 1
    paused = False
    cursor_pos = 0
    cursor_max_pos = 0
    info = {}
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
        elif key == ord("k"):
            scr.addstr(3, 0, 'Specify the id process to kill : ')
            scr.move(3, 33)
            scr.nodelay(0)
            curses.echo()
            scr.refresh()
            pids = scr.getstr().split()
            for pid in pids:
                try:
                    sql.execute('kill ' + pid)
                except MySQLdb.OperationalError as e:
                    scr.move(3,0)
                    scr.clrtoeol()
                    scr.addstr(3, 0, '%s' % (e))
                    scr.refresh()
                    time.sleep(1)
            curses.noecho()
            scr.nodelay(1)
            scr.refresh()
        elif key == ord("f"):
            scr.addstr(3, 0, 'filter : ')
        elif key == ord("p"):
            if paused:
                paused = False
                delay_counter = delay
                scr.erase()
            else:
                scr.addstr(3, 0, 'Pause', curses.A_BLINK)
                display_process(scr, process, cursor_pos)
                display_footer(scr, " [u]p  [d]own  [i]nfo  [q]uit")
                scr.refresh()
                paused = True
                scr.nodelay(0)
                curses.curs_set(0)
                while paused:
                    key = scr.getch()
                    if key == curses.KEY_DOWN:
                        if cursor_pos < len(process) - 1:
                            cursor_pos = cursor_pos + 1
                        display_process(scr, process, cursor_pos)
                        scr.refresh()
                    elif key == curses.KEY_UP:
                        if cursor_pos > 0:
                            cursor_pos = cursor_pos - 1
                        display_process(scr, process, cursor_pos)
                        scr.refresh()
                    elif key == ord("i"):
                        display_details(scr, process[cursor_pos])
                        scr.erase()
                        display_header(scr, info)
                        display_process(scr, process, cursor_pos)
                        display_footer(scr, " [u]p  [d]own  [i]nfo  [q]uit")
                    elif key == ord("q"):
                        paused = False
                        scr.nodelay(1)
                        curses.curs_set(1)
                        scr.move(3, 0)
                        scr.refresh()
                          
        if delay_counter  == delay and not paused:
            delay_counter = 0                   
                    
            try:
                scr.erase()
                sql.execute('select VERSION();')
                info["version"] = sql.fetchone()[0]
                info["user"] = user
                sql.execute('show status where Variable_name="Uptime"')
                info["uptime"] = str(datetime.timedelta(seconds = int(sql.fetchone()[1])))
                sql.execute('SHOW PROCESSLIST;')
                display_header(scr, info)
                process = []
                try:
                    for row in sql.fetchall():
                        if len(str(row[5])) > 8 :
                            row[5] = "-"
                        if row[3] is None:
                            dbName = "None"
                        else:
                            dbName = row[3]

                        if row[4].lower().strip() == 'query':
                            state = "Q"
                        elif row[4].lower().strip() == 'sleep':
                            state = "S"
                        elif row[4].lower().strip() == 'connect':
                            state = "C"
                        elif row[4].lower().strip() == 'bindlog':
                            state = "B"
                        else:
                            state = "U"
                        if row[7] is None:
                            query = "None"
                        else:
                            query = row[7]

                        #query = query.rstrip("\n")

                        p = [row[0], row[1], row[2].split(':')[0], dbName, state, row[5], query]
                        process.append(p)

                    display_process(scr, process)
                    display_footer(scr, " [d]elay  [f]ilter  [H]ighlight  [k]ill  [h]elp  [q]uit")
                except curses.error: pass
                except IOError: pass
                scr.move(3, 0)
                #scr.refresh()
            except KeyboardInterrupt:
                sys.exit(-1)
        else:
            delay_counter = delay_counter + 0.5
            
        time.sleep(0.5)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    options = arg_parser()
    try:
        db = MySQLdb.connect(host=options["host"], user=options["user"], passwd=options["password"], port=options["port"])
    except MySQLdb.OperationalError as e:
        print e[1]
        sys.exit(1)
    else:
        curses.wrapper(getStats, options["user"], db)


