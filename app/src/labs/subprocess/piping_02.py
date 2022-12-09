# See https://linuxhint.com/python-subprocess-pipes/

import sys
print ("what is your name?")
for name in iter(sys.stdin.readline, ''):
    name = name[:-1]
    if name == "exit":
        break
    print ("Well, how are you {0}?".format(name))
    print ("\n What is your name?")