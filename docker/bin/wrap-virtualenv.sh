#!/bin/bash

# Activate virtualenv
echo -n "Bootstrapping virtualenv wrapper ... "
source /usr/local/bin/virtualenvwrapper.sh
echo "done"
echo -n "Activating environment $VIRTUALENV_NAME ... "
workon $VIRTUALENV_NAME
echo done

# Run command
echo "Running command '$@'"
exec $@
