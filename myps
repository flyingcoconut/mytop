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

import sys
import signal
import getopt
import datetime


try: #try to import sqltoplib
    import sqltoplib
except ImportError:
    print "sqltoplib library is missing"
    sys.exit(1)

VERSION = "0.0.1"

def signal_handler(sig, frame):
    """
    Get signals and exit
    """
    sys.exit(1)

def show_usage():
    """
    Print a usage message
    """
    print """Usage: myps [OPTION]... -u [USER]...
    """

def show_help():
    """Print a help message"""
    print """Database process viewer
Example: myps -u root -h localhost -p password --type mysql

Options:
  -b, --BACKEND=BACKEND     set the backend type (mysql, mongodb, pgsql)
  -h, --host=HOSTNAME       set hostname
  -l, --list                list all type
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

def main(pm=None):
    pm.refresh()
    print "%-10s %-11s %-15s %-20s %-5s %-8s %-5s" % ('ID', 'USER', 'HOST', 'DB', 'STATE', 'TIME', 'INFO')
    for process in pm.process:
        print "%-10s %-11s %-15s %-20s %-5s %-8s %-5s" % (process.pid, process.user[:10], process.host.split(':')[0][:15], process.db[:20], process.state, process.time, process.info[:44])



if __name__ == '__main__':
    #Initialise signal to catch SIGINT
    signal.signal(signal.SIGINT, signal_handler)
    #Call the parser function
    args = arg_parser()
    #Try to connect to the MySQL server
    pm = sqltoplib.create_connection(backend=args["backend"], host=args["host"], user=args["user"], password=args["password"], port=args["port"])
    try:
        pm.connect()
    except sqltoplib.processmanager.ProcessManagerError as e:
        print e
        sys.exit(1)
    main(pm)


