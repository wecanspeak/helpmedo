#!/usr/bin/env python3

import os
import sys
import getopt
from utils.color import TextColor as Color
from utils.package import check_necessary_pkg
from importlib import import_module
from colorama import init as color_init
from utils.jobctrl import Scenario

color_init()
gJobs = {}
gActions = {}

def usage():
    print("""
Usage: %s [-hl] project job [action [sth]]

       -h, --help      Display this message
       -l, --listjob   List jobs
    """ % sys.argv[0])

def build_all_jobs():
    global gJobs, gActions
    gJobs = {}
    for root, dirs, files in os.walk("."):
        dirs.sort()
        path = root.split("." + os.sep + "job" + os.sep)
        if len(path) != 2:
            continue
        proj = path[1]
        for filename in files:
            if filename.endswith('.py'):
                if proj not in gJobs:
                    gJobs[proj] = []
                job = filename[:-3]
                gJobs[proj].append(job)
                s = Scenario(proj, job)
                acts = s.get_action()
                if acts:
                    gActions[proj + job] = acts
                else:
                    gActions[proj + job] = None

def list_job():
    print("")
    for proj, jobs in gJobs.items():
        print("PROJECT: " + Color.PROJECT + proj + Color.ENDC)
        for job in jobs:
            print("    JOB:" + Color.JOB, end='')
            print(" " + job + Color.ENDC)
            print(" ACTION:" + Color.ACTION, end='')
            if gActions[proj + job]:
                for act in gActions[proj + job]:
                    print(" " + act["name"], end=',')
            else:
                print(" - ", end='')
            print("\b", end='')
            print(" ", end='')
            print(Color.ENDC)
        print(" ")

def validate_job(proj, job):
    if proj not in gJobs:
        return 0
    if job not in gJobs[proj]:
        return 0
    return 1

def parse_args(argv):
    proj = job = ""
    action = []
    try:
        opts, args = getopt.getopt(argv, "hl", ["help", "listjob"])
    except getopt.GetoptError:
        sys.exit(1)

    if not argv:
        usage()
        sys.exit(1)

    if len(args) >= 2:
        proj = args[0]
        job = args[1]

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-l", "--listjob"):
            list_job()
            sys.exit(0)

    if not validate_job(proj, job):
        print("\nNot supported job \"" + Color.JOB + "%s" % job + Color.ENDC
              + "\" for project \"" + Color.PROJECT + "%s" % proj + Color.ENDC + "\"\n")
        sys.exit(1)

    action.extend(args[2:4])

    return proj, job, action

def apply_job(scenario, proj, job, action):
    pkg = "job." + proj + "." + job
    obj = import_module(pkg)
    Job = getattr(obj, "Job")
    job = Job(proj, job)
    if job.setup(scenario):
        print("Job setup failed!")
        return -1
    if job.execute(action):
        print("Job execution failed!")
        return -1
    if job.report(None):
        print("Job report failed!")
        return -1
    return 0

if __name__ == "__main__":
    build_all_jobs()
    proj, job, action = parse_args(sys.argv[1:])
    s = Scenario(proj, job)
    check_necessary_pkg(s)
    apply_job(s, proj, job, action)
