from zope.interface import implementer
from utils.jobctrl import IJob
import os
import requests

@implementer(IJob)
class Job(object):
    s = result = None

    def __init__(self, proj, job):
        pass

    def setup(self, scenario):
        self.s = scenario.get_all()
        return 0

    def execute(self, action=None):
        matched = 0
        self.result = 0
        for act in self.s["action"]:
            if action and action[0] == act["name"]:
                matched = 1
                if act["with"] != "" and len(action) < 2:
                    return -3

                if action[0] == "ls":
                    os.system("ls -al")
                elif action[0] == "echo":
                    os.system("echo " + action[1])
                elif action[0] == "web_request":
                    try:
                        r = requests.get(action[1])
                        print(r)
                    except Exception:
                        self.result = -1

        if not matched:
            return -2
        else:
            return 0

    def report(self, method):
        if self.result:
            print("Action failed!")
        else:
            print("Action done successfully.")
        return 0
