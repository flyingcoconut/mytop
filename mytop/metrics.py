class Gauge(object):
    def __init__(self, name, minimum, maximum, value):
        self.name = name
        self.minimum = minimum
        self.maximum = maximum
        self.value = value
        self.enable = False

    def enable(self):
        self.enable = True

    def disable(self):
        self.enable = False

    def update(self, value):
        self.value = value
        self.percent = None

    def to_dict(self):
        d = {
          "name": self.name,
          "minimum": self.minimum,
          "maximum": self.maximum,
          "value": self.value,
          "percent": (self.value / self.maximum) * 100
        }
        return d

class Counter(object):
    def __init__(self, name, function):
        self.name = name
        self.value = None
        self.enable = False

    def enable(self):
        self.enable = True

    def disable(self):
        self.enable = False

    def update(self, value):
        self.value = value
        self.percent = None

    def to_dict(self):
        d = {
          "name": self.name,
          "value": self.value
        }
        return d

class Label(object):
    def __init__(self, name, default=None):
        self.name = name
        self.value = default
        self.enable = False

    def enable(self):
        self.enable = True

    def disable(self):
        self.enable = False

    def update(self, value):
        self.value = value

    def to_dict(self):
        d = {
          "name": self.name,
          "value": self.value
        }
        return d


class Table(object):
    def __init__(self, name, column_name=[], column_type=[], function=None):
        self.name = name
        self.column_name = column_name
        self.column_type = column_type
