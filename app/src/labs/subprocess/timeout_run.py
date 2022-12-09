# See https://alexandra-zaharia.github.io/posts/kill-subprocess-and-its-children-on-timeout-python/

import subprocess

cmd = ['/path/to/cmd', 'arg1', 'arg2']  # the external command to run
timeout_s = 10  # how many seconds to wait 

try:
    p = subprocess.run(cmd, timeout=timeout_s)
except subprocess.TimeoutExpired:
    print(f'Timeout for {cmd} ({timeout_s}s) expired')