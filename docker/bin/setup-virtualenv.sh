#!/bin/bash

function create_virtualenv() {
    mkdir -p $WORKON_HOME
    mkvirtualenv $VIRTUALENV_NAME
}

# Setup virtualenvwrapper
source /usr/local/bin/virtualenvwrapper.sh

# Create virtualenv directory if not exists
test -d $WORKON_HOME/$VIRTUALENV_NAME || create_virtualenv

# Activate the virtualenv
workon $VIRTUALENV_NAME

# Install application dependencies
pip install -r requirements.txt
