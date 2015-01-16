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
"""Linux Driver"""
import datetime
import platform

import driver
import psutil


class LinuxProcessDriver(driver.Driver):
    """Linux Process Driver"""
    def __init__(self):
        driver.Driver.__init__(self)
        self.name = "linux:process"

    def fields(self):
        """
        Return all disponible fields
        """
        fields = {}
        fields["pid"] = int
        fields["user"] = str
        fields["state"] = str
        fields["time"] = str
        fields["info"] = str
        return fields

    def tops(self):
        """Linux process"""
        all_process = []
        for pr in psutil.process_iter():
            p = {}
            p["pid"] = pr.pid
            p["user"] = pr.username
            p["nice"] = pr.nice
            memory = pr.get_ext_memory_info()
            p["rss"] = memory[0]
            p["vms"] = memory[1]
            p["shared"] = memory[2]
            p["state"] = self._get_process_status(pr.status)
            p["cpu"] = pr.get_cpu_percent(0)
            p["memory"] = pr.get_memory_percent()
            p["time"] = pr.create_time
            p["command"] = pr.name
            all_process.append(p)
        return all_process

    def info(self):
        info = {}
        f = open("/proc/uptime")
        proc_uptime = float(f.read().split()[0])
        f.close()
        info["uptime"] = str(datetime.timedelta(seconds = int(proc_uptime)))
        info["swap"] = psutil.swap_memory()
        info["load"] = psutil.os.getloadavg()
        info["version"] = platform.release()
        return info

    def kill(self, process, signal):
        process = psutil.Process(process.pid)
        process.send_signal(signal)

    def renice(self, process, nice):
        process = psutil.Process(process.pid)
        process.set_nice(nice)

    def _get_process_status(self, status):
        if status == psutil.STATUS_SLEEPING:
            return "Sleeping"
        else:
            return status

class LinuxDiskDriver(driver.Driver):
    """Linux Disk Driver"""
    def __init__(self):
        driver.Driver.__init__(self)
        self.name = "linux:disk"

    def fields(self):
        """
        Return all disponible fields
        """
        fields = {}
        fields["pid"] = int
        fields["user"] = str
        fields["state"] = str
        fields["time"] = str
        fields["info"] = str
        return fields

    def tops(self):
        """Linux process"""
        all_disk = []
        iostats = psutil.disk_io_counters(True)
        #partitions = psutil.disk_partitions(False)
        for disk in iostats:
            d = dict(iostats[disk]._asdict())
            d["partition"] = disk
            all_disk.append(d)
        return all_disk

    def info(self):
        pass

class LinuxNetworkDriver(driver.Driver):
    """Linux Network Driver"""
    def __init__(self):
        driver.Driver.__init__(self)
        self.name = "linux:network"

    def fields(self):
        """
        Return all disponible fields
        """
        fields = {}
        fields["pid"] = int
        fields["user"] = str
        fields["state"] = str
        fields["time"] = str
        fields["info"] = str
        return fields

    def tops(self):
        """Linux process"""
        all_nics = []
        network = psutil.net_io_counters(pernic=True)
        for nic in network:
            n = dict(network[nic]._asdict()) #Convert namedtuple into dict
            n["interface"] = nic
            all_nics.append(n)
        return all_nics

    def info(self):
        pass
