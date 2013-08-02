#mytop#

mytop is a console-based tool for monitoring and managing process from different databases server.
It is possible to monitor, filter, and kill process from different backend.
It runs on most Unix systems (including Mac OS X) which have python and curses.
It could possibly run on Windows.

![ScreenShot](https://raw.github.com/flyingcoconut/mytop/master/mytop.png)


##Features##

- Delay beetween process refresh
- Process history
- Filter based on regexp
- Multiple backend connexion at the same time
- Dump a list of process to file
- Pause
- Get more details about a specific process
- Display stats from the backend


##Backend##

Here is the list of disponible backend


###mysql###

Status : stable

Dependency : MySQLdb


###redisdb###

Status : beta

Dependency : redis-py


###mongodb###

Status : beta

Dependency : PyMongo

###mssql###

Status : todo

Dependency : Unknown

###pgsql###

Status : todo

Dependency : Psycopg


Beware this software is in early alpha stage !

