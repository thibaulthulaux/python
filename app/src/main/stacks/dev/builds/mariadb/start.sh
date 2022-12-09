#!/usr/bin/env bash

echo "${HOSTNAME}:$0: >> Begin."

set -e

[ "${DEBUG}" == 'true' ] && set -x

# Start mariadb service
runuser mysql -c 'mariadb'

# mariadb user=root

echo "${HOSTNAME}:$0: >> Terminate."

exec "$@"
