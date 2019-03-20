from zope.interface import implementer
from utils.jobctrl import IJob
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from shutil import copy
import sys
import os
import time
import logging

class Handler(FileSystemEventHandler):
    dst_dir = None
    def __init__(self, dst_dir):
        FileSystemEventHandler.__init__(self)
        self.dst_dir = dst_dir

    def on_any_event(self, event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s" % event.src_path)
        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print("Received modified event - %s" % event.src_path)
            print("File size %d " % os.path.getsize(event.src_path))
            time.sleep(5)
            copy(event.src_path, self.dst_dir)
            print("Copy file done")

@implementer(IJob)
class Job(object):
    s = observer = observe_dir = dest_dir = None
    def __init__(self, proj, job):
        self.observer = Observer()
        pass

    def setup(self, scenario):
        self.s = scenario.get_all()
        self.observe_dir = self.s["observe_dir"]
        self.dest_dir = self.s["destination_dir"]
        if not self.observe_dir:
            try:
                if sys.platform == "win32":
                    self.observe_dir = os.getenv("OBSERVE_DIR")
                else:
                    self.observe_dir = os.environ["OBSERVE_DIR"]
            except Exception:
                pass
        if not self.observe_dir:
            self.observe_dir = '.'
            print("Observe directory is PWD")
        else:
            print("Observe directory is " + self.observe_dir)
        return 0

    def _update_notify(self, fpath):
        print("Press CTRL-C to cancel.")
        event_handler = Handler(self.dest_dir)
        self.observer.schedule(event_handler, self.observe_dir, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()
        pass

    def execute(self, action=None):
        matched = 0
        self.result = self._update_notify(None)
        return 0

    def report(self, method):
        if self.result:
            print("Action failed!")
        else:
            print("Action done successfully.")
        return 0
