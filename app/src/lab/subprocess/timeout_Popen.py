# See https://alexandra-zaharia.github.io/posts/kill-subprocess-and-its-children-on-timeout-python/

import os
import signal
import subprocess
import sys

cmd = ['/path/to/cmd', 'arg1', 'arg2']  # the external command to run
timeout_s = 10  # how many seconds to wait 

try:
    p = subprocess.Popen(cmd, start_new_session=True)
    p.wait(timeout=timeout_s)
except subprocess.TimeoutExpired:
    print(f'Timeout for {cmd} ({timeout_s}s) expired', file=sys.stderr)
    print('Terminating the whole process group...', file=sys.stderr)
    os.killpg(os.getpgid(p.pid), signal.SIGTERM)