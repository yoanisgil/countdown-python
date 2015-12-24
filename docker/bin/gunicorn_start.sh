#!/bin/bash

NAME="${APP_NAME:-app}"                           # Name of the application
DJANGODIR=/srv/app                                # Django project directory
SOCKFILE=/var/run/gunicorn.sock                   # we will communicte using this unix socket
USER=www-data                                     # the user to run as
GROUP=www-data                                    # the group to run as
NUM_WORKERS="${NUM_WORKERS:-3}"                   # how many worker processes should Gunicorn spawn
WSGI_APP="${WSGI_APP:-application}"               # WSGI application object
export PYTHONUNBUFFERED="True"                    # Disable stdin/stdout buffering.

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /usr/local/bin/virtualenvwrapper.sh
workon $VIRTUALENV_NAME
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${WSGI_MODULE}:${WSGI_APP} \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=info \
  --log-file=/dev/stdout
