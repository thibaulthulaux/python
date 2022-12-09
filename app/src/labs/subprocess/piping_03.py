# See https://linuxhint.com/python-subprocess-pipes/

import subprocess
import sys

proc = subprocess.Popen(["python", "CallMyName.py "])

while proc.returncode is None:
    proc.poll()

proc = subprocess.Popen(["python", "CallMyName.py "],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE)

proc.stdin.write("Alex\n")
proc.stdin.write("Jhon\n")
proc.stdin.close()

while proc.returncode is None:
    proc.poll()

print ("I am back from the child program this:\n{0}".format(proc.stdout.read()))