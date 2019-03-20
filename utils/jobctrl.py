import yaml
import os
import sys
from zope.interface import Interface

class JobErrCode:
    OK = 0
    FAIL = -1
    ACTION_NOT_FOUND = -2
    ACTION_ARGS = -3

# Interface for all kinds of jobs
class IJob(Interface):
    def setup(scenario):
        """ job setup """
    def execute(action):
        """ job execute """
    def report(method):
        """ job report """

# Job scenario
class Scenario():
    s = None

    def __init__(self, proj, job):
        with open("job" + os.sep + proj + os.sep + job + ".yml", 'r') as stream:
            try:
                self.s = yaml.load(stream)
            except yaml.YAMLError:
                print("\"" + job + ".yml\" does not follow YAML format. Abort.")
                sys.exit(1)

    def get_all(self):
        return self.s

    def get_job_description(self):
        if "job_description" in self.s:
            return self.s["job_description"]
        else:
            return None

    def get_required_pkg(self):
        if "required_python_pkg" in self.s:
            return self.s["required_python_pkg"]
        else:
            return None

    def get_action(self):
        if "action" in self.s:
            return self.s["action"]
        else:
            return None
