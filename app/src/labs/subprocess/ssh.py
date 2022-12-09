import subprocess
import sys

host = "toto@machine_b.fr"

command = "ls"

ssh = subprocess.Popen(["ssh", "%s" % host, command],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
result = ssh.stdout.readlines()
if result == []:
    error = ssh.stderr.readlines()
    print("ERROR: %s" % error )
else:
    print( result )