from zope.interface import implementer
from utils.jobctrl import IJob
from slackclient import SlackClient
import sys
import os

@implementer(IJob)
class Job(object):
    s = api_token = user_id = result = None
    def __init__(self, proj, job):
        pass

    def setup(self, scenario):
        self.s = scenario.get_all()
        self.api_token = self.s["slack_api_token"]
        self.user_id = self.s["slack_user_id"]
        if not self.api_token or not self.api_token:
            try:
                if sys.platform == "win32":
                    self.api_token = os.getenv("SLACK_API_TOKEN")
                    self.user_id = os.getenv("SLACK_USER_ID")
                else:
                    self.api_token = os.environ["SLACK_API_TOKEN"]
                    self.user_id = os.environ["SLACK_USER_ID"]
            except Exception:
                pass
        if not self.api_token:
            print("slack_api_token is not set")
            return -1
        if not self.user_id:
            print("slack_user_id is not set")
            return -1
        return 0

    def _send_msg(self, msg):
        sc = SlackClient(self.api_token)
        r = sc.api_call(
                "chat.postMessage",
                channel=self.user_id,
                text=msg,
                as_user=1
                )
        if not r["ok"]:
            return -1
        else:
            return 0

    def execute(self, action=None):
        matched = 0
        self.result = 0
        for act in self.s["action"]:
            if action and action[0] == act["name"]:
                matched = 1
                if act["with"] != "" and len(action) < 2:
                    return -3

                if action[0] == "send_msg":
                    self.result = self._send_msg(action[1]) \
                                  if act["with"] and len(action) > 1 else -1

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
