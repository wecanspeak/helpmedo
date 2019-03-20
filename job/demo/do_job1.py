from zope.interface import implementer
from utils.jobctrl import IJob

@implementer(IJob)
class Job(object):
    def __init__(self, proj, job):
        pass

    def setup(self, scenario):
        print("job1 setup done")
        return 0

    def execute(self, action=None):
        print("job1 executed")
        return 0

    def report(self, method):
        print("job1 reported")
        return 0
