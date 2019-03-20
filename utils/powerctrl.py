from zope.interface import Interface
from zope.interface import implementer
import requests
import os
import sys
import subprocess

# Interface for all kinds of power controller
class IPowerCtrl(Interface):
    def setup(scenario):
        """ setup power controller """
    def power_on(ports):
        """ power on """
    def power_off(ports):
        """ power off """

# ports format "1,2,3,4"
def parse_port(ports):
    return ports.split(",")

# Aviosys IP Power 9528-T
@implementer(IPowerCtrl)
class IP9258(object):
    ACTION_GOOD = 0
    ACTION_FAIL = -1
    ip = account = pw = None

    def __init__(self, ip, account, pw):
        self.ip = ip
        self.account = account
        self.pw = pw

    def _check_ping(self, ip):
        if sys.platform == "win32":
            FNULL = open(os.devnull, "w")
            response = subprocess.call(["ping", "-n", "1", ip], stdout=FNULL, 
                                       stderr=subprocess.STDOUT)
        else:
            response = os.system("ping -c 1 " + ip + " >/dev/null 2>&1")
        if response == 0:
            return self.ACTION_GOOD
        else:
            return self.ACTION_FAIL

    def _power_ctrl(self, ports, onoff):
        pl = parse_port(ports)
        sstr = gstr = ""
        gpl = []
        for p in pl:
            if int(p) < 5 and int(p) > 0:
                sstr += ("+p6" + p + "=" + onoff)
                gpl.append("p6" + p + "=" + onoff)
        r = requests.get(url="http://" + self.ip + "/set.cmd?user=" + \
                self.account + "+pass=" + str(self.pw) + "cmd=setpower" + sstr)
        for pl in gpl:
            if not pl in r.text:
                return self.ACTION_FAIL
        return self.ACTION_GOOD

    def setup(self, scenario):
        return self._check_ping(self.ip)

    def power_on(self, ports):
        return self._power_ctrl(ports, "1")

    def power_off(self, ports):
        return self._power_ctrl(ports, "0")
