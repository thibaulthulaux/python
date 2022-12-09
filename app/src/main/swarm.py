#!/usr/bin/env python3
"""
Module Docstring
"""

""" IMPORTS --------------------------------------------------------------- """
import argparse
import logging # see https://docs.python.org/3/library/logging.html
import logging.config
import os
import platform
import signal
import subprocess
import sys
import time
# import docker
# import pprint # pretty print for dict()

""" GLOBAL VARIABLES ------------------------------------------------------ """
# Default LOGLEVEL
os.environ['LOGLEVEL'] = 'DEBUG'

# System
__env__ = os.environ
__start__ = time.time()
__platform__ = platform.system()

# Authoring
__author_name__ = 'Thibault HULAUX'
__author_mail__ = 'thibault.hulaux@gmail.com'
__version__ = '0.1.0'
__license__ = 'MIT'

# Magic file and folder paths
__basename__ = os.path.basename(__file__)
__basenamenoext__ = __basename__.split(".", 1)[0]
__dirname__ = os.path.dirname(__file__)

# Help strings
__description__ = f'{__basename__} is a python helper script to administrate a docker swarm and docker services.'
__epilog__ = f'Run {__basename__} [command] --help for more information on a command.'

""" INITIALIZE WORKING DIRECTORY ------------------------------------------ """
# Change working directory to script location
os.chdir(__dirname__)

""" INITIALIZE LOGGER ----------------------------------------------------- """
log = None

# Add log filepath and filename to the logging namespace, so the config file
# can reference it.
logging.filepath = 'log'
logging.filename = f'{__basenamenoext__}.log'

# Load config file
logging.config.fileConfig(
  fname='conf/logging.conf',
  disable_existing_loggers=False
  )

# Create logger
log = logging.getLogger(__basename__)

""" INITIALIZE PARSER ----------------------------------------------------- """
parser = None

# Create parser
parser = argparse.ArgumentParser(
  add_help = True,
  formatter_class = argparse.RawDescriptionHelpFormatter,
  description=__description__,
  epilog=__epilog__
)

# Add parser arguments
parser.add_argument(
  '-d', '--debug',
  action='store_true',
  default=False
)
parser.add_argument(
  '--version',
  action='version',
  version=f'{__basename__} (version {__version__}) {__author_name__} - {__author_mail__}'
)

# Initialize subparsers
subparsers = parser.add_subparsers(dest='subcommand', help='Commands')

def argument(*name_or_flags, **kwargs):
    """Helper function to satisfy argparse.ArgumentParser.add_argument()'s
    input argument syntax.

    """
    return (list(name_or_flags), kwargs)

def subcommand(args=[], parent=subparsers):
    """Decorator to define a new subcommand in a sanity-preserving way.
    See https://mike.depalatis.net/blog/simplifying-argparse.html

    """
    def decorator(func):
        parser = parent.add_parser(func.__name__, description=func.__doc__)
        for arg in args:
            parser.add_argument(*arg[0], **arg[1])
        parser.set_defaults(func=func)
    return decorator

# 'swarm' subcommands definition
@subcommand([
  argument('command', help='Commands', choices=[
    'create', 'remove', 'start', 'status', 'stop', 'update'
    ])
  ])
def swarm(args):
    '''swarm subcommand definition'''
    cmd = args.command
    list = get_listfromfile('conf/swarm.conf')
    if cmd == 'create':
        swarm_create(list)
        swarm_config_network(list)
        # swarm_config_nfs(list)
        swarm_register(list)
    if cmd == 'remove':
        # swarm_stop(list)
        swarm_remove(list)
        swarm_cleanup(list)
    if cmd == 'start':
        swarm_start(list)
        # swarm_config_network(list)
        # swarm_register(list)
    if cmd == 'status':
        swarm_status(list)
    if cmd == 'stop':
        swarm_stop(list)
    if cmd == 'update':
        # swarm_config_network(list)
        swarm_config_nfs(list)
        # swarm_config_extras(list)
        # swarm_register(list)

# 'stack' subcommands definition
@subcommand([
  argument('command', help='Commands', choices=['deploy', 'remove', 'start', 'stop']),
  argument('stack', help='stack name', choices=['all', 'core', 'dev', 'monitoring', 'pipeline'])
  ])
def stack(args):
    '''stack subcommand definition'''
    cmd = args.command
    stack = args.stack
    list = get_listfromfile('conf/stacks.conf')
    for hostname in get_listfromfile('conf/swarm.conf'):
        if 'manager' in hostname: manager = hostname
    if cmd == 'deploy':
        if stack == 'all':
            stack_deploy_list(list, manager)
        else: stack_deploy(stack, manager)
    if cmd == 'remove':
        if stack == 'all':
            list.reverse()
            stack_remove_list(list, manager)
        else: stack_remove(stack, manager)
    # if cmd == 'start': stack_start(args.stack)
    # if cmd == 'stop': stack_stop(args.stack)

""" CORE FUNCTIONS -------------------------------------------------------- """
def get_listfromfile(path):
    """'get_listfromfile(path)' Returns non commented lines from file as list.
    
    """
    path = get_realpath(path)
    file = open(path, 'r')
    result = []
    for line in file.readlines():
        line = line.strip()
        if line == '' or line.startswith('#') or line.startswith(';'): continue
        result.append(line)
    return result

def get_exec(name):
    """'get_exec(name)' Returns program absolute path.
    
    """
    # TODO: cache program paths
    global DOCKER
    global MACHINE
    global VBOX


    if name == 'docker':
        if __platform__ == 'Windows':
            cmd = ['C:\Windows\System32\where.exe', 'docker.exe']
            proc = subprocess_run(cmd)
            path = proc.stdout.strip()
        else: pass

    if name == 'machine':
        if __platform__ == 'Windows':
            path = f'{__dirname__}/bin/docker-machine-Windows-0.16.2x86_64.exe'
        else:
            path = 'bin/docker-machine-Linux-0.16.2x86_64'

    if name == 'vbox':
        if __platform__ == 'Windows': pass
        else: pass

    return get_realpath(path)

def get_realpath(path):
    """"""
    if not os.path.exists(path):
        log.error(f'{path} does not exist.')
        sys.exit(1)
    return os.path.realpath(path)

""" SUBPROCESS FUNCTIONS --------------------------------------------------- """
def subprocess_run(cmd, timeout_s=180, input=None):
    """_summary_

    Args:
        cmd (_type_): _description_
        timeout_s (int, optional): _description_. Defaults to 180.
        input (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    log.debug(f'subprocess_run(cmd={cmd}, timeout_s={timeout_s}, input={input})')
    try:
        # proc = subprocess.run(cmd, input=input, timeout=timeout_s, capture_output=True, text=True, shell=True)
        proc = subprocess.run(cmd, input=input, timeout=timeout_s, capture_output=True, text=True)
    except subprocess.TimeoutExpired:
        log.error(f'timeout for cmd={cmd} ({timeout_s}s) expired.')
        sys.exit(1)
    stdout = []
    for line in proc.stdout.splitlines():
        stdout.append(line)
    stderr = []
    for line in proc.stderr.splitlines():
        stderr.append(line)
    log.debug(f'stdout={stdout}, stderr={stderr}')
    return proc

def subprocess_prun(cmd, list, timeout_s=180):
    ''' Run a command on each host as parallelized subprocesses.
        - Args:
          - cmd: list of commands to run as subprocess
          - list: list of hostnames
          - timeout_s: timeout in seconds (default=120)
        - Returns:
          - proc: completed processes
    '''
    log.debug(f'subprocess_prun(cmd={cmd}, list={list}, timeout_s={timeout_s})')
    processes = []
    for hostname in list:
        log.info(f'{hostname}: Running subprocess...')
        path = f'log/{hostname}.log'
        out = open(path, 'a')
        cmdline = cmd + [hostname]
        log.debug(f'cmdline={cmdline} log={path}')
        proc = subprocess.Popen(cmdline, stdout=out, stderr=out)
        processes.append((proc, out))
    for proc, out in processes:
        try:
            proc.wait(timeout=timeout_s)
        except subprocess.TimeoutExpired:
            log.error(f'timeout for {cmd} ({timeout_s}s) expired.')
            log.debug(f'terminating process {proc.pid}.')
            os.kill(proc.pid, signal.SIGTERM)
        finally:
            out.close()
    return processes

""" SYSTEM FUNCTIONS ----------------------------------------------------- """
def system_sanitize():
    ''''''
    # subprocess.call(['runas', '/user:Administrator', 'myfile.exe'])
    # taskkill.exe /f /im "VBox*"; taskkill.exe /f /im "virtualbox.exe"
    pass

def system_check():
    ''''''
    status = False
    # TODO: Check requirements (docker + virtualbox)
    return status

def system_init():
    ''''''
    # TODO: Initialize system ?
    pass

''' Run as admin
import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    # Code of your program here
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
'''


""" MACHINE FUNCTIONS ----------------------------------------------------- """
def machine_env(hostname: str) -> list:
    """Get docker environment from machine hostname.

    Args:
        hostname (str): machine hostname

    Returns:
        list: docker environment as ([key, value])
    """
    log.debug(f'{hostname}: getting machine environment')
    cmd = [get_exec('machine'), 'env', hostname]
    proc = subprocess_run(cmd)
    env = []
    for line in proc.stdout.splitlines():
        if line.startswith('REM') or line.startswith('#'): continue
        line = line.replace('$Env:', '').replace('SET ', '')
        key = line.split('=', 1)[0].strip()
        value = line.split('=', 1)[1].strip()
        env.append([key, value])
    log.debug(f'hostname={hostname}, env={env}')
    return env

def machine_activate(hostname: str):
    """Set docker environment from machine hostname.

    Args:
        hostname (str): machine
    """
    env = machine_env(hostname)
    log.debug(f'{hostname}: Setting machine environment')
    os.environ = __env__
    for key, value in env:
        os.environ[key] = value

def machine_ip(hostname: str) -> str:
    """Returns ip from docker machine hostname.

    Args:
        hostname (str): docker machine hostname

    Returns:
        str: "external" ip address (NAT).
    """
    log.debug(f'{hostname}: Getting machine ip')
    cmd = [get_exec('machine'), 'ip', hostname]
    proc = subprocess_run(cmd)
    ip = proc.stdout.strip()
    log.debug(f'hostname={hostname}, ip={ip}')
    return ip

def machine_swarm_leave(hostname: str):
    """_summary_

    Args:
        hostname (str): _description_
    """
    machine_activate(hostname)
    log.debug(f'{hostname}: Leaving swarm')
    cmd = [get_exec('docker'), 'swarm', 'leave', '--force']
    proc = subprocess_run(cmd)

def machine_swarm_init(hostname, ip):
    """'machine_leaveswarm(hostname)' documentation.
    
    """
    machine_activate(hostname)
    log.info(f'{hostname}: Initializing swarm')
    cmd = [get_exec('docker'), 'swarm', 'init', '--advertise-addr', ip]
    proc = subprocess_run(cmd)
    cmd = [get_exec('docker'), 'swarm', 'join-token', '-q', 'worker']
    proc = subprocess_run(cmd)
    token = proc.stdout.strip()
    return token

def machine_swarm_join(hostname, token, manager):
    """'machine_leaveswarm(hostname)' documentation.
        manager: ip:port 
    
    """
    machine_activate(hostname)
    log.info(f'{hostname}: Joining swarm')
    cmd = [get_exec('docker'), 'swarm', 'join', '--token', token, manager]
    proc = subprocess_run(cmd)

def machine_ssh(hostname, cmd):
    ''''''
    cmd = [get_exec('machine'), 'ssh', hostname, cmd]
    return subprocess_run(cmd)

""" SWARM FUNCTIONS ------------------------------------------------------- """
# def swarm_info():
    # cmd = "watch 'echo --- IP && ip addr | grep eth1 | grep inet && echo --- NODE && docker node ls && echo --- STACK && docker stack ls && echo --- SERVICE && docker service ls && echo --- IMAGE && docker image ls && echo --- NETWORK  && docker network ls && echo --- VOLUME && docker volume ls'"

def swarm_cleanup(list):
    """'swarm_cleanup(list)' documentation.
    
    """
    log.info('> Cleaning up...')
    log.debug(f'list={list}')
    for i in list:
        file = get_realpath(f'log/{i}.log')
        log.debug(f'Removing {file}')
        os.remove(file)
    for i in os.listdir(f'tmp'):
        file = get_realpath(f'tmp/{i}')
        log.debug(f'Removing {file}')
        os.remove(file)
    log.info('> System clean.')

def swarm_create(list):
    """'swarm_create(list)' documentation.
    
    """
    log.info('> Creating swarm... (This may take several minutes)')
    log.debug(f'list={list}')
    if __platform__ == 'Windows':
        options = get_listfromfile('conf/driver-windows-virtualbox.conf')
    cmd = [get_exec('machine')] + ['create'] + options
    processes = subprocess_prun(cmd, list, 120)
    log.info(f'> {len(list)} machines created.')

def swarm_register(list):
    """'swarm_register(list)' documentation.
    
    """
    log.info('> Registering swarm...')
    log.debug(f'list={list}')
    manager = ''
    port = '2377'
    token = ''
    for hostname in list:
        machine_activate(hostname)
        machine_swarm_leave(hostname)
        if 'manager' in hostname:
            ip = machine_ip(hostname)
            manager = f'{ip}:{port}'
            log.debug(f'manager={manager}')
            token = machine_swarm_init(hostname, ip)
        else:
            machine_swarm_join(hostname, token, manager)
    log.info(f'> {len(list)} nodes registered.')

def swarm_remove(list):
    """'swarm_remove(list)' documentation.
    
    """
    log.info('> Removing swarm...')
    log.debug(f'list={list}')
    cmd = [get_exec('machine')] + ['rm', '-f']
    processes = subprocess_prun(cmd, list)
    log.info(f'> {len(list)} machines removed.')

def swarm_config_network(list):
    """'swarm_setup(list)' documentation.
    
    """
    log.info('> Setting up network...')
    log.debug(f'list={list}')
    # Create temporary hosts file
    local_path = 'tmp/hosts'
    file = open(local_path, 'w')
    file.write('# /etc/hosts\n')
    for hostname in list:
        ip = machine_ip(hostname)
        line = f'{ip} {hostname}'
        log.debug(f'Adding line={line} to {local_path}')
        file.write(f'{line}\n')
    file.close()
    # Write to each host
    tag = f'# Added by {__basename__}:swarm_config_network()'
    remote_path = '/etc/hosts'
    for hostname in list:
        log.info(f'{hostname}: Edit {remote_path}')
        # Remove previous appends depending on tag
        cmd = ''
        cmd += 'i=1; while read line; do '
        cmd += 'if [ "$line" == "'+ tag +'" ]; then break; fi; i=$((i+1)); '
        cmd += 'done < /etc/hosts; '
        cmd += 'head -n $((i-1)) /etc/hosts | sudo tee /etc/hosts'
        proc = machine_ssh(hostname, cmd)
        # Append host definitions
        cmd = '{ echo "' + tag + '"; '
        for line in get_listfromfile(local_path):
            if line.endswith(hostname): continue
            cmd = cmd + 'echo "' + line + '"; '
        cmd = cmd + '} | sudo tee -a /etc/hosts'
        proc = machine_ssh(hostname, cmd)
    log.info('> Network setup complete.')

def swarm_config_extras(list):
    '''
    '''
    log.info('> Installing extras...')
    log.debug(f'list={list}')
    for hostname in list:
        # Install nmap
        log.info(f'{hostname}: Install nmap')
        cmd = 'tce-load -wi nmap'
        proc = machine_ssh(hostname, cmd)
    log.info('> extras setup complete.')


def swarm_config_nfs(list):
    '''
    '''
    log.info('> Setting up nfs...')
    log.debug(f'list={list}')
    for hostname in list:
        # Install nfs-utils
        log.info(f'{hostname}: Install nfs-utils')
        cmd = 'tce-load -wi nfs-utils'
        proc = machine_ssh(hostname, cmd)
        if 'manager' in hostname:
            # Install filesystems extension
            log.info(f'{hostname}: Install filesystems extension')
            # cmd = 'tce-load -wi filesystems-4.19.10-tinycore64'
            cmd = 'tce-load -wi filesystems-KERNEL'
            proc = machine_ssh(hostname, cmd)
            # Enable nfs-server
            log.info(f'{hostname}: Enable nfs-server')
            cmd = 'sudo ln -s /usr/local/etc/init.d/nfs-server /sbin; sudo nfs-server start'
            proc = machine_ssh(hostname, cmd)
            # Create /data structure
            log.info(f'{hostname}: Create /data structure')
            folders = [
              '/data/core/registry',
              '/data/env/{dev,prod,staging}/mariadb',
              '/data/monitoring/{grafana,prometheus}',
              '/data/pipeline/gitlab-runner'
            ]
            cmd = 'sudo mkdir -p'
            for path in folders:
                cmd += f' {path}'
            cmd += '; sudo chown nobody:nogroup'
            for path in folders:
                cmd += f' {path}'
            proc = machine_ssh(hostname, cmd)
            # Edit nfs exports
            remote_path = '/usr/local/etc/exports'
            log.info(f'{hostname}: Edit {remote_path}')
            tag = f'# Added by {__basename__}:swarm_config_nfs()'
            exports = [
              ['/data/core/registry', '(rw,sync)'],
              ['/data/env/dev/mariadb', '(rw,sync,no_root_squash)'],
              ['/data/env/prod/mariadb', '(rw,sync,no_root_squash)'],
              ['/data/env/staging/mariadb', '(rw,sync,no_root_squash)'],
              ['/data/monitoring/grafana', '(rw,sync,all_squash)'],
              ['/data/monitoring/prometheus', '(rw,sync)'],
              ['/data/pipeline/gitlab-runner', '(rw,sync)']
            ]
            cmd = '{ echo "' + tag + '";'
            for export in exports:
                cmd += f' echo "{export[0]}'
                for host in list:
                    # if 'manager' in host: continue
                    cmd += f' {host}{export[1]}'
                cmd += '";'
            cmd += ' } | sudo tee ' + remote_path
            proc = machine_ssh(hostname, cmd)
            # Export nfs
            log.info(f'{hostname}: Export nfs')
            cmd = 'sudo exportfs -arv'
            proc = machine_ssh(hostname, cmd)
        else:
            log.info(f'{hostname}: Enable nfs-client')
            cmd = 'sudo ln -s /usr/local/etc/init.d/nfs-client /sbin; sudo nfs-client start'
            proc = machine_ssh(hostname, cmd)
    log.info('> nfs setup complete.')

def swarm_start(list):
    """'swarm_start(list)' documentation.
    
    """
    log.info('> Starting machines...')
    log.debug(f'list={list}')
    cmd = [get_exec('machine')] + ['start']
    processes = subprocess_prun(cmd, list, 300)
    log.info(f'> {len(list)} started.')

def swarm_status(list):
    """'swarm_status(list)' documentation.
    
    """
    log.info('> Checking status...')
    log.debug(f'list={list}')
    status = False

    cmd = [get_exec('machine')] + ['ls']
    processes = subprocess_prun(cmd, list)
    for proc in processes:
        pass
    log.info(f'{status}')
    return status

def swarm_stop(list):
    """'swarm_stop(list)' documentation.
    
    """
    log.info('> Stopping machines...')
    log.debug(f'list={list}')
    cmd = [get_exec('machine')] + ['stop']
    processes = subprocess_prun(cmd, list, 300)
    log.info(f'> {len(list)} machines stopped.')

""" STACK FUNCTIONS ------------------------------------------------------- """
def compose_convert():
    ''''''
    version = '3.6'

    cmd = [get_exec('docker'), 'compose', 'convert']
    proc = subprocess_run(cmd)

    # 'docker compose convert' needs serious fixing...
    # 1. add mandatory compose version.
    compose = f"version: '{version}'\n"
    for line in proc.stdout.splitlines():
        # 2. remove conflicting name entry.
        if line.startswith('name') : continue
        # 3. remove '"' to define integers.
        if 'published' in line : line = line.replace('"', '')
        compose = compose + f'{line}\n'

    return compose

def stack_volumes_create():
    ''''''
    pass

def stack_volumes_remove():
    ''''''
    pass

def stack_networks_create():
    ''''''
    pass

def stack_networks_remove():
    ''''''
    pass

def service_build(stack, manager):
    ''''''
    log.debug(f'stack={stack}, manager={manager}')
    log.info(f'{stack}: Building stack.')


    log.info(f'{stack}: Stack built.')

def stack_deploy(stack, manager):
    '''Deploy a single docker stack on swarm manager.'''
    log.debug(f'stack={stack}, manager={manager}')
    log.info(f'{stack}: Deploying stack.')

    # Setup working directory and environment
    os.chdir(f'{__dirname__}/stacks/{stack}')
    machine_activate(manager)

    # Add environment variables
    env = [
      ('STACK', stack),
      ('MANAGER', manager)
    ]
    for key, value in env:
        os.environ[key] = value

    # If stack contains builds
    if os.path.isdir('builds'):
        for build in os.listdir('builds'):
            log.debug(f'build={build}')
            # Build image
            log.info(f'{stack}: Building {build}.')
            cmd = [get_exec('docker'), 'build', '-t', f'127.0.0.1:5000/{stack}-{build}', f'builds/{build}/.']
            proc = subprocess_run(cmd, timeout_s=240)
            # Push image to registry
            log.info(f'{stack}: Pushing {build}.')
            cmd = [get_exec('docker'), 'push', f'127.0.0.1:5000/{stack}-{build}:latest']
            proc = subprocess_run(cmd, timeout_s=240)

    # Deploy stack
    compose = compose_convert()
    cmd = [get_exec('docker'), 'stack', 'deploy', '--compose-file', '-', stack]
    proc = subprocess_run(cmd, input=compose)

    # Revert working directory and environment
    os.chdir(__dirname__)
    os.environ = __env__
    log.info(f'{stack}: Stack deployed.')

def stack_remove(stack, manager):
    '''Remove a single docker stack from swarm manager.'''
    log.debug(f'stack={stack}, manager={manager}')
    log.info(f'{stack}: Removing stack.')

    # Setup working directory and environment
    os.chdir(f'{__dirname__}/stacks/{stack}')
    machine_activate(manager)

    # Adding environment variables
    env = [
      ('STACK', stack),
      ('MANAGER', manager)
    ]
    for key, value in env:
        os.environ[key] = value

    # Remove stack
    log.info(f'{stack}: Remove services.')
    cmd = [get_exec('docker'), 'stack', 'rm', stack]
    proc = subprocess_run(cmd)

    # # Wait for complete service shutdown
    # time.sleep(5.0)

    # # Remove volumes
    # log.info(f'{stack}: Remove volumes.')
    # cmd = [get_exec('docker'), 'compose', 'convert', '--volumes']
    # proc = subprocess_run(cmd)
    # for volume in proc.stdout.splitlines():
    #     cmd = [get_exec('docker'), 'volume', 'rm', '--force', f'{stack}_{volume}']
    #     proc = subprocess_run(cmd)

    # Revert working directory and environment
    os.chdir(__dirname__)
    os.environ = __env__
    log.info(f'{stack}: Stack removed.')

def stack_deploy_list(list, manager):
    '''Deploy docker stacks from list on swarm manager.'''
    log.info('> Deploying stacks...')
    log.debug(f'list={list}, manager={manager}')
    for stack in list:
        stack_deploy(stack, manager)
    log.info(f'> {len(list)} stacks deployed.')

def stack_remove_list(list, manager):
    '''Remove docker stacks from list on swarm manager.'''
    log.info('> Removing stacks...')
    log.debug(f'list={list}, manager={manager}')
    for stack in list:
        stack_remove(stack, manager)
    log.info(f'> {len(list)} stacks removed.')

""" MAIN FUNCTION --------------------------------------------------------- """
def main():
    ''' Main entry point'''
    # Parse args
    args = parser.parse_args()
    log.debug(f'args={args}, args.subcommand={args.subcommand}')
    if args.subcommand is None:
        parser.print_help()
    else:
        args.func(args)

    # Debug:
    # print("User's Environment variable:")
    # pprint.pprint(dict(__env__), width = 1)

    # Execution time
    log.debug(f'Execution time: {(time.time()-__start__)*10**3:.03f} ms')

""" RUNTIME --------------------------------------------------------------- """
if __name__ == '__main__':
    ''' This is executed when run from the command line '''
    main()
sys.exit(0)
