#mytop#

mytop is a console-based tool for monitoring and managing process from different databases server.
It is possible to monitor, filter, and kill process from different backend.
It runs on most Unix systems (including Mac OS X) which have python and curses.

![ScreenShot](https://raw.github.com/flyingcoconut/mytop/master/mytop.png)


##Features##

- Delay
- Process history
- Filter based on regexp
- Multiple backend connexion at the same time
- Dump to file
- Pause
- Get more details about specific process
- Display stats from the backend
- Fullscreen mode


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


###linux###

Status : beta

Dependency : psutil

###mssql###

Status : todo

Dependency : Unknown

###pgsql###

Status : todo

Dependency : Psycopg



Beware this software is in early alpha stage !

