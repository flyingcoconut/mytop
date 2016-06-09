import selectors
import sys
import os
import subprocess
import sched
import json

class Session(object):
    def __init__(self, driver_path):
        self._driver_path = driver_path
        self._process = None
        self.interval = 5
        self.state = None
        self.version = None
        self.author = None
        self.name = None

    def get_configurations(self):
        """Get all possible configuration"""
        self._send_rpc_call("getconfigs")
        self._recv_rpc_resp()

    def update_configurations(self):
        """Update driver configuration"""
        self._send_rpc_call("setconfigs")

    def collect(self):
        """Collect all metrics"""
        self._send_rpc_call("collect")

    def list_metrics(self):
        """List possible metrics"""
        self._send_rpc_call("listmetrics")

    def enable_metric(self, metric):
        """Enable a specific metric"""
        self._send_rpc_call("enablemetric", metric)

    def disable_metric(self, metric):
        """Disable a specific metric"""
        self._send_rpc_call("disablemetric", metric)
        self._recv_rpc_resp()

    def list_actions():
        pass

    def initialize():
        """Initialize driver after configuration"""
        self._send_rpc_call("init")

    def load(self):
        """Start driver subprocess"""
        self._process = subprocess.Popen([self._driver_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        informations = self._process.stdout.read(1024)
        print(informations)

    def terminate():
        """Ask driver to terminate politely"""
        self._send_rpc_call("term")
        self._recv_rpc_call()
        self._process.terminate()

    def _recv_informations(self):
        """Receive driver initial informations"""
        pass

    def _send_rpc_call(self, method, params={}, timeout=10):
        msg = {
          "method": method,
          "params": params
        }
        print(json.dumps(msg))

    def _recv_rpc_resp(self, timeout):
        print("Receiving")
    

class SessionManager(object):
    def __init__(self):
        self._sessions = []
        self._selector = selectors.DefaultSelector()
        self._sched = sched.scheduler(time.time, time.sleep)

    def new_session(self, driver_path):
        session = Session(driver_path)
        self._sessions.append(session)

    def list_sessions(self):
        return self._sessions

    def list_drivers(self):
        pass

    def start_collection(self):
        pass

    def _read(self, conn, mask):
        """Read data from stdin fd"""
        data = os.read(sys.stdin.fileno(), 1)
        print(data)
