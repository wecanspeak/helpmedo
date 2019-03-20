from utils.jobctrl import Scenario
from helpmedo import apply_job

def test_unit_test():
    test_jobs = [
            {"proj": "demo", "job": "do_job1", "action": None},
            {"proj": "demo", "job": "do_job2", "action": ["ls"]},
            {"proj": "demo", "job": "do_job2", "action": ["echo", "hello world"]},
            ]
    for j in test_jobs:
        s = Scenario(j["proj"], j["job"])
        print("proj {} job {}".format(j["proj"], j["job"]))
        assert apply_job(s, j["proj"], j["job"], j["action"]) == 0
