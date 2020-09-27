#!/bin/bash

#to rollback, run: sudo userdel -r fileshare

# create service user
useradd --create-home --comment "Account for running fileshare app" --shell /bin/bash fileshare

# make new virtual environment
python3 -m venv /home/fileshare/venv

# activate it
source "/home/fileshare/venv/bin/activate"

# install the dependencies
pip install -r requirements.txt

# copy unit file to systemd's dir
cp file_api/fs.service /etc/systemd/system

# copy source files to service user's home
cp -a file_api /home/fileshare

# ensure the correct ownership
chown -R fileshare:fileshare /home/fileshare

# restart systemd to make new service found
systemctl daemon-reload