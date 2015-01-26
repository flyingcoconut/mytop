#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Patrick Charron
# Email : patrick.charron.pc@gmail.com
# Description : Top Informations Viewer
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
import platform

from . import driver
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
        for item in psutil.process_iter():
            process = {}
            process["pid"] = item.pid
            process["user"] = item.username()
            process["nice"] = item.nice()
            memory = item.get_ext_memory_info()
            process["rss"] = memory[0]
            process["vms"] = memory[1]
            process["shared"] = memory[2]
            process["state"] = item.status()
            process["cpu"] = item.get_cpu_percent(0)
            process["memory"] = item.get_memory_percent()
            process["time"] = item.create_time()
            process["command"] = item.name()
            all_process.append(process)
        return all_process

    def info(self):
        pass

    def kill(self, process, signal):
        """Kill a process"""
        process = psutil.Process(process.pid)
        process.send_signal(signal)

    def renice(self, process, nice):
        """Renice a process"""
        process = psutil.Process(process.pid)
        process.set_nice(nice)


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
        all_disks = []
        iostats = psutil.disk_io_counters(True)
        partitions = self._get_partitions()
        for disk in iostats:
            new_disk = dict(iostats[disk]._asdict())
            try:
                new_disk.update(partitions["/dev/" + disk])
            except KeyError:
                new_disk["mountpoint"] = "-"
                new_disk["fstype"] = "-"
                new_disk["opts"] = "-"
            new_disk["device"] = disk
            all_disks.append(new_disk)
        return all_disks

    def _get_partitions(self):
        """Get partitions informations"""
        partitions = {}
        for partition in psutil.disk_partitions(False):
            informations = dict(partition._asdict())
            del informations["device"]
            partitions[partition.device] = informations
        return partitions

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
        network = psutil.network_io_counters(pernic=True)
        for nic in network:
            new_nic = dict(network[nic]._asdict()) #Convert namedtuple into dict
            new_nic["interface"] = nic
            all_nics.append(new_nic)
        return all_nics

    def info(self):
        pass

class LinuxSocketDriver(driver.Driver):
    """Linux Network Driver"""
    def __init__(self):
        driver.Driver.__init__(self)
        self.name = "linux:socket"

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
        all_sockets = []
        sockets = psutil.net_connections("all")
        for socket in sockets:
            sock = {}
            sock["fd"] = socket.fd
            sock["family"] = self._get_family(socket.family)
            sock["type"] = self._get_type(socket.type)
            sock["laddr"] = socket.laddr
            #sock["sport"] = socket.laddr[1]
            sock["raddr"] = socket.raddr
            #sock["rport"] = socket.raddr[1]
            sock["status"] = socket.status
            sock["pid"] = socket.pid
            all_sockets.append(sock)
        return all_sockets

    def _get_family(self, family):
        """Return family string"""
        families = {
            1 : "AF_UNIX",
            2 : "AF_INET",
            10: "AF_INET6"
        }
        try:
            return families[family]
        except KeyError:
            return family

    def _get_type(self, stype):
        """Get socket type string"""
        stypes = {
            1 : "STREAM",
            2 : "DGRAM"
        }
        try:
            return stypes[stype]
        except KeyError:
            return stype

    def info(self):
        pass

class LinuxCpuDriver(driver.Driver):
    """Linux Network Driver"""
    def __init__(self):
        driver.Driver.__init__(self)
        self.name = "linux:cpu"

    def fields(self):
        pass

    def tops(self):
        """Linux process"""
        all_cpus = []
        cpus_time = psutil.cpu_times_percent(0, True)
        for cpu_time in enumerate(cpus_time):
            cpu = {}
            cpu["cpu"] = cpu_time[0]
            cpu["user"] = cpu_time[1].user
            cpu["nice"] = cpu_time[1].nice
            cpu["system"] = cpu_time[1].system
            cpu["idle"] = cpu_time[1].idle
            cpu["iowait"] = cpu_time[1].iowait
            cpu["irq"] = cpu_time[1].irq
            cpu["softirq"] = cpu_time[1].softirq
            cpu["steal"] = cpu_time[1].steal
            cpu["guest"] = cpu_time[1].guest
            cpu["guest_nice"] = cpu_time[1].guest_nice
            all_cpus.append(cpu)
        return all_cpus

    def info(self):
        pass
