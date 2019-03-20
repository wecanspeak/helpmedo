from zope.interface import implementer
from utils.jobctrl import IJob
from utils.powerctrl import IP9258

@implementer(IJob)
class Job(object):
    s = pwrctrl = result = None

    def __init__(self, proj, job):
        pass

    def setup(self, scenario):
        self.s = scenario.get_all()
        self.pwrctrl = IP9258(self.s["power_control"]["ip"],
                              self.s["power_control"]["account"],
                              self.s["power_control"]["password"])
        if self.pwrctrl.setup(scenario) == IP9258.ACTION_FAIL:
            print("Setup {} failed.".format(self.s["power_control"]["device"]))
            return -1
        return 0

    def execute(self, action=None):
        matched = 0
        self.result = 0
        for act in self.s["action"]:
            if action and action[0] == act["name"]:
                matched = 1
                if act["with"] != "" and len(action) < 2:
                    return -3
                try:
                    action_method = getattr(self.pwrctrl, action[0])
                except AttributeError:
                    print("IP9258 does not yet implement action \"" +
                          action[0] + "\"")
                    return -1
                if act["with"]:
                    self.result = action_method(action[1])
                else:
                    self.result = action_method()
                return self.result

        if not matched:
            return -2
        else:
            return 0

    def report(self, method):
        device = self.s["power_control"]["device"]
        if self.result == IP9258.ACTION_GOOD:
            print("Control {} successfully.".format(device))
        else:
            print("Control {} failed!".format(device))
        return 0
