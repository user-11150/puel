#!/usr/bin sh

# Configure the Git

python ./tools/configure_git.py

# Install Python requirements

sh install-requirements.sh dev
sh install-requirements.sh docs


