#!/usr/bin/env sh
set -e

npm run build
<<<<<<< HEAD
source ./shell_scripts/auto_pipenv.sh
auto_pipenv_shell
=======
>>>>>>> 4a790e3ec4a00a3fcbff3ad0e4f39125ce6763e5

if [ $# -eq 0 ] || [ "${1#-}" != "$1" ]; then
  set -- supervisord "$@"
fi

exec "$@"
