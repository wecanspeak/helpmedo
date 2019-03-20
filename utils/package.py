import subprocess
import re
import sys

pkgs = ""
def check_pkg(mypkg):
    global pkgs
    if not pkgs:
        if sys.platform == "win32":
            pkgs = subprocess.run(["python", "-m", "pip", "list"], stdout=subprocess.PIPE).stdout.\
                    decode('utf-8')
        else:
            pkgs = subprocess.run(["pip", "list"], stdout=subprocess.PIPE).stdout.\
                    decode('utf-8')
    if re.search(mypkg, pkgs):
        return 1
    return 0

def check_necessary_pkg(s):
    pkglist = ["zope.interface", "colorama", "PyYAML"]
    if s.get_required_pkg():
        pkglist.extend(s.get_required_pkg())
    for pkg in pkglist:
        if pkg and not check_pkg(pkg):
            print("Failed. \"" + pkg + "\" package is not installed.")
            sys.exit(1)
