_drivers = {}

try:
    import linux
except:
    pass
else:
    _drivers.update(linux.drivers)

try:
    import mysql
except:
    pass
else:
    _drivers.update(mysql.drivers)

try:
    import redisdb
except:
    pass
else:
    _drivers.update(redisdb.drivers)


def list():
    return _drivers.keys()

def load(driver):
    return _drivers[driver]()


