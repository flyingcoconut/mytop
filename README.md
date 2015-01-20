#mytop#

mytop is a console-based tool for monitoring, watching, recording and managing top informations from different sources.
It runs on most Unix systems (including Mac OS X) which have python and curses.

![ScreenShot](https://raw.github.com/flyingcoconut/mytop/master/mytop.png)


##Features##

- Refresh delay
- Top informations history
- Filter based on regexp
- Multiple drivers
- Write to file
- Pause
- Record and play
- Display stats from the drivers
- Fullscreen mode


##Drivers##

Here is the list of disponible drivers


###mysql###

Status : stable

Dependency : MySQLdb


###redisdb###

Status : beta

Dependency : redis-py


###mongodb###

Status : beta

Dependency : PyMongo


###linux:process###

Status : beta

Dependency : psutil

###linux:cpu###

Status : beta

Dependency : psutil

###mssql###

Status : todo

Dependency : Unknown

###pgsql###

Status : todo

Dependency : Psycopg

###apache###

Status : todo

Dependency : mod_status on apache

Beware this software is in early alpha stage !
