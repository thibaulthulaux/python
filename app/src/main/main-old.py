#!/usr/bin/env python3
"""
Module Docstring
"""

""" ----------------------------------------------------------------------- """
# Importing
import argparse
import logging # see https://docs.python.org/3/library/logging.html
import logging.config
import os
import platform
import subprocess
import sys
# import docker
# import pprint # pretty print for dict()

""" ----------------------------------------------------------------------- """
# Intializing global variables
__author__ = "Thibault HULAUX"
__version__ = "0.0.1"
__license__ = "MIT"

__env__ = os.environ
__dirname__ = os.path.dirname(__file__)
__basename__ = os.path.basename(__file__)
__basenamenoext__ = __basename__.split(".", 1)[0]
__description__ = f"{__basename__} is python helper script"

# Changing working directory to script location
os.chdir(__dirname__)

""" ----------------------------------------------------------------------- """
# Initializing logger
logger = None

# Add log filepath and filename to the logging namespace, so the config file can reference it.
logging.filepath = "log"
logging.filename = str(f"{__basenamenoext__}.log")

# Load config file
logging.config.fileConfig(
  fname="conf/logging.conf",
  disable_existing_loggers=False
  )
# Create logger
logger = logging.getLogger(__basename__)

""" ----------------------------------------------------------------------- """
def readLines(path):
    file = open(path, 'r')

    lines = list()

    for line in file.readlines():
        if line.startswith('#') or line == '': continue
        line = line.strip()
        lines.append(line)
    # lines = open(path, "r").read().splitlines()
    return lines

def getRealPath(path):
    result = os.path.realpath(path)
    return result

""" ----------------------------------------------------------------------- """
# Subcommand machine
def machines_create(host_list):
    logger.info('Creating machines...')
    logger.debug(f'host_list={host_list}')
    options = [
      'create',
      '--virtualbox-no-vtx-check',
      '--driver=virtualbox',
      '--engine-opt',
      'experimental',
      '--engine-opt',
      'metrics-addr=0.0.0.0:4999'
    ]
    processes = []
    for host in host_list:
        logger.info(f'[{host}]')
        out = open(f'log/{host}.log', 'a')
        cmdline = [MACHINE] + options + [host]
        proc = subprocess.Popen(cmdline, stdout=out, stderr=out)
        processes.append((proc, out))
    for proc, out in processes:
        proc.wait()
        out.close()
    logger.info('Creation complete.')

def machines_register(host_list):
    logger.info('Registering machines...')
    logger.debug(f'host_list={host_list}')
    port = '2377'

    host_file = open('tmp/hosts', 'w')
    host_file.truncate(0)

    for host in host_list:
        # docker-machine ip target
        logger.info(f'[{host}] Getting ip')
        options = ['ip']
        cmdline = [MACHINE] + options + [host]
        proc = subprocess.run(cmdline, capture_output=True, text=True, shell=True)
        logger.debug(proc.stdout)
        logger.debug(proc.stderr)
        ip = proc.stdout.strip()
        logger.debug(f'ip={ip}')
        host_file.write(f'{ip} {host}\n')

        # docker-machine env target
        logger.info(f'[{host}] Getting docker environment')
        options = ['env']
        cmdline = [MACHINE] + options + [host]
        proc = subprocess.run(cmdline, capture_output=True, text=True, shell=True)
        logger.debug(proc.stdout)
        logger.debug(proc.stderr)
        env = []
        for line in proc.stdout.splitlines():
            if line.startswith('REM') or line.startswith('#'): continue
            line = line.replace('$Env:', '').replace('SET ', '')
            key = line.split('=', 1)[0].strip()
            value = line.split('=', 1)[1].strip()
            env.append([key, value])

        logger.info(f'[{host}] Applying docker environment.')
        os.environ = __env__
        for key, value in env:
          os.environ[key] = value

        logger.info(f'[{host}] Leaving existing swarm.')
        options = ['swarm', 'leave', '--force']
        cmdline = [DOCKER] + options
        proc = subprocess.run(cmdline, capture_output=True, text=True, shell=True)
        logger.debug(proc.stdout)
        logger.debug(proc.stderr)

        if 'manager' in host:
          manager = ip + ':' + port
          logger.debug(f'manager={manager}')

          # docker swarm init
          logger.info(f'[{host}] Initializing swarm.')
          options = ['swarm', 'init', '--advertise-addr', ip]
          cmdline = [DOCKER] + options
          proc = subprocess.run(cmdline, capture_output=True, text=True, shell=True)
          logger.debug(proc.stdout)
          logger.debug(proc.stderr)

          # docker swarm join-token
          logger.info(f'[{host}] Retrieving token.')
          options = ['swarm', 'join-token', '-q', 'worker']
          cmdline = [DOCKER] + options
          proc = subprocess.run(cmdline, capture_output=True, text=True, shell=True)
          logger.debug(proc.stdout)
          logger.debug(proc.stderr)
          token = proc.stdout.strip()
          logger.debug(f'token={token}')

        else:
          worker = ip + ':' + port
          logger.debug(f'[{host}] worker = {worker}')

          # docker swarm join
          logger.info(f'[{host}] Joining swarm.')
          options = ['swarm', 'join', '--token', token]
          cmdline = [DOCKER] + options + [manager]
          proc = subprocess.run(cmdline, capture_output=True, text=True, shell=True)
          logger.debug(proc.stdout)
          logger.debug(proc.stderr)

    host_file.close()
    logger.info('Registration complete.')

def machines_setup(host_list):
    logger.info('Setting up machines...')
    logger.debug(f'host_list={host_list}')

    for host in host_list:
        logger.info(f'[{host}] Setting up /etc/hosts')

        # Remove lines from "# added by __basename__" in /etc/hosts
        command = 'i=1; while read line; do if [ "$line" == "# added by '+ __basename__ +'" ]; then break; fi; i=$((i+1)); done < /etc/hosts; head -n $((i-1)) /etc/hosts | sudo tee /etc/hosts'
        options = ['ssh']
        cmdline = [MACHINE] + options + [host] + [command]
        proc = subprocess.run(cmdline, capture_output=True, text=True, shell=True)
        logger.debug(proc.stdout)
        logger.debug(proc.stderr)

        # Add lines to /etc/hosts from tmp/hosts
        lines = readLines('tmp/hosts')
        hosts = []
        for line in lines:
            if line.endswith(host): continue
            hosts.append(line)
        logger.debug(f'hosts={hosts}')

        command = '{ echo "# added by '+ __basename__ +'"; '
        for line in hosts:
          command = command + 'echo "' + line + '"; '
        command = command + '} | sudo tee -a /etc/hosts'
        logger.debug(f'command={command}')

        options = ['ssh']
        cmdline = [MACHINE] + options + [host] + [command]
        proc = subprocess.run(cmdline, capture_output=True, text=True, shell=True)
        logger.debug(proc.stdout)
        logger.debug(proc.stderr)

    # Install and start nfs-server / nfs-client
    for host in host_list:
        logger.info(f'[{host}] Setting up nfs.')
        command = 'tce-load -wi nfs-utils'
        options = ['ssh']
        cmdline = [MACHINE] + options + [host] + [command]
        proc = subprocess.run(cmdline, capture_output=True, text=True, shell=True)
        logger.debug(proc.stdout)
        logger.debug(proc.stderr)
        if 'manager' in host:
            # create folder structure for data on manager
            command = 'sudo mkdir -p /data/core/registry /data/environments/dev/mariadb /data/environments/prod/mariadb /data/environments/staging/mariadb /data/monitoring/grafana /data/monitoring/prometheus /data/pipeline/gitlab-runner; sudo chown nobody:nogroup /data/core/registry /data/environments/dev/mariadb /data/environments/prod/mariadb /data/environments/staging/mariadb /data/monitoring/grafana /data/monitoring/prometheus /data/pipeline/gitlab-runner'
            options = ['ssh']
            cmdline = [MACHINE] + options + [host] + [command]
            proc = subprocess.run(cmdline, capture_output=True, text=True, shell=True)
            logger.debug(proc.stdout)
            logger.debug(proc.stderr)
            # Install and start nfs-server
            command = 'sudo ln -s /usr/local/etc/init.d/nfs-server /sbin; sudo nfs-server start'
        else:
            # Install and start nfs-client
            command = 'sudo ln -s /usr/local/etc/init.d/nfs-client /sbin; sudo nfs-client start'
        options = ['ssh']
        cmdline = [MACHINE] + options + [host] + [command]
        proc = subprocess.run(cmdline, capture_output=True, text=True, shell=True)
        logger.debug(proc.stdout)
        logger.debug(proc.stderr)
        if 'manager' in host:
            # Editing /etc/exports
            command = 'ls'
            options = ['ssh']
            cmdline = [MACHINE] + options + [host] + [command]
            proc = subprocess.run(cmdline, capture_output=True, text=True, shell=True)
            logger.debug(proc.stdout)
            logger.debug(proc.stderr)
            # Exporting nfs
            command = 'sudo exportfs -av'
            options = ['ssh']
            cmdline = [MACHINE] + options + [host] + [command]
            proc = subprocess.run(cmdline, capture_output=True, text=True, shell=True)
            logger.debug(proc.stdout)
            logger.debug(proc.stderr)

    logger.info('Setup complete.')

"""
# Core
/data/core/registry thx-swarm-01(rw,sync)
# Pipeline
/data/pipeline/gitlab-runner thx-swarm-01(rw,sync)
# Monitoring
/data/monitoring/prometheus thx-swarm-01(rw,sync)
/data/monitoring/grafana thx-swarm-01(rw,sync,all_squash)
# Environments
/data/environments/dev/mariadb thx-swarm-01(rw,sync,no_root_squash) thx-swarm-02(rw,sync,no_root_squash) thx-swarm-03(rw,sync,no_root_squash)   
/data/environments/staging/mariadb thx-swarm-01(rw,sync,no_root_squash) thx-swarm-02(rw,sync,no_root_squash) thx-swarm-03(rw,sync,no_root_squash)
/data/environments/prod/mariadb thx-swarm-01(rw,sync,no_root_squash) thx-swarm-02(rw,sync,no_root_squash) thx-swarm-03(rw,sync,no_root_squash)  
"""




def machines_remove(host_list):
    logger.info('Removing machines...')
    logger.debug(f'host_list={host_list}')
    options = ['rm', '-f']
    processes = []
    for host in host_list:
        logger.info(f'[{host}]')
        out = open(f'log/{host}.log', 'a')
        cmdline = [MACHINE] + options + [host]
        proc = subprocess.Popen(cmdline, stdout=out, stderr=out)
        processes.append((proc, out))
    for proc, out in processes:
        proc.wait()
        out.close()
    logger.info('Machines removed.')

def machines_start(host_list):
    logger.info('Starting machines...')
    logger.debug(f'host_list={host_list}')
    options = ['start']
    processes = []
    for host in host_list:
        logger.info(f'[{host}]')
        out = open(f'log/{host}.log', 'a')
        cmdline = [MACHINE] + options + [host]
        proc = subprocess.Popen(cmdline, stdout=out, stderr=out)
        processes.append((proc, out))
    for proc, out in processes:
        proc.wait()
        out.close()
    logger.info('Machines started.')

def machines_stop(host_list):
    logger.info('Stopping machines...')
    logger.debug(f'host_list={host_list}')
    options = ['stop']
    processes = []
    for host in host_list:
        logger.info(f'[{host}]')
        out = open(f'log/{host}.log', 'a')
        cmdline = [MACHINE] + options + [host]
        proc = subprocess.Popen(cmdline, stdout=out, stderr=out)
        processes.append((proc, out))
    for proc, out in processes:
        proc.wait()
        out.close()
    logger.info('Machines stopped.')

""" ----------------------------------------------------------------------- """
# Subcommand stack
def stacks_deploy(stack_list):
    logger.info('Deploying stacks...')

    for stack in stack_list:
        logger.info(f'({stack})')
        os.chdir(f'{__dirname__}/stacks/{stack}')
        options = ['compose', 'convert']
        cmdline = [DOCKER] + options
        proc = subprocess.run(cmdline, capture_output=True, text=True, shell=True)
        compose = proc.stdout
        logger.debug(f'{compose}')


    os.chdir(__dirname__)
    exit()


def stack_remove():
    logger.debug("stack_remove")

""" ----------------------------------------------------------------------- """
# Initializing parser
parser = None
subparser = None

# Initialize parser
parser = argparse.ArgumentParser(
  add_help = True,
  formatter_class = argparse.RawDescriptionHelpFormatter,
  description=__description__,
  epilog=f"""Run {__basename__} [command] --help for more information on a command."""
)

# Add parser arguments
parser.add_argument(
  "-d", "--debug",
  action="store_true",
  default=False
)
parser.add_argument(
  "--version",
  action="version",
  version=f"%(prog)s (version {__version__}) {__author__}"
)

# Initialize subparsers
subparsers = parser.add_subparsers(dest="subcommand", help="Commands")

""" ----------------------------------------------------------------------- """
def argument(*name_or_flags, **kwargs):
    """Helper function to satisfy argparse.ArgumentParser.add_argument()'s
    input argument syntax"""
    return (list(name_or_flags), kwargs)

def subcommand(args=[], parent=subparsers):
    """Decorator to add to functions.
    See https://mike.depalatis.net/blog/simplifying-argparse.html
    """
    def decorator(func):
        parser = parent.add_parser(func.__name__, description=func.__doc__)
        for arg in args:
            parser.add_argument(*arg[0], **arg[1])
        parser.set_defaults(func=func)
    return decorator

""" ----------------------------------------------------------------------- """
@subcommand([
  argument('command', help='Commands', choices=[
    'create', 'register', 'remove', 'setup', 'start', 'stop'
    ])
  ])
def machines(args):
    host_list = readLines('machines/list')
    command = args.command
    if command == 'create': machines_create(host_list)
    if command == 'register': machines_register(host_list)
    if command == 'remove': machines_remove(host_list)
    if command == 'setup': machines_setup(host_list)
    if command == 'start': machines_start(host_list)
    if command == 'stop': machines_stop(host_list)

@subcommand([
  argument('command', help='Commands', choices=['deploy', 'remove'])
  ])
def stacks(args):
    stack_list = readLines('stacks/list')
    command = args.command
    if command == 'deploy': stacks_deploy(stack_list)
    if command == 'remove': stacks_remove(stack_list)

""" ----------------------------------------------------------------------- """
def main():
    """ Main entry point of the app """

    """ Select docker-machine and docker binary files depending on host platform
    and set them as global variables """
    global MACHINE
    global DOCKER

    if platform.system() == "Windows":
        MACHINE = getRealPath("bin/docker-machine-Windows-0.16.2x86_64.exe")
        proc = subprocess.run(["C:\Windows\System32\where.exe", "docker.exe"], capture_output=True, text=True)
        DOCKER = getRealPath(proc.stdout.strip())
    else:
        MACHINE = getRealPath("bin/docker-machine-Linux-0.16.2x86_64")
        proc = subprocess.run(["/user/bin/which", "docker"], capture_output=True, text=True)
        DOCKER = getRealPath(proc.stdout.strip())

    """ Parse args """
    args = parser.parse_args()
    if args.subcommand is None:
        parser.print_help()
    else:
        args.func(args)

    """ Debug """
    # logger.debug(f"Args: {args}")
    # logger.debug(f"Subparser: {args.subcommand}")
    # print("User's Environment variable:")
    # pprint.pprint(dict(__env__), width = 1)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()

sys.exit(0)
