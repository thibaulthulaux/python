#!/usr/bin/env bash

echo "${HOSTNAME}:$0: >> Begin."

set -e

[ "${DEBUG}" == 'true' ] && set -x

# BAse image Ubuntu 22.04 uses sysvinit init system
# User following instead of `systemctl enable --now ssh`
service ssh start

# Start tomcat service
catalina.sh run

# mariadb user=root

echo "${HOSTNAME}:$0: >> Terminate."

exec "$@"
