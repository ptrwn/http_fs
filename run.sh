#!/bin/bash

# to remove -- sudo userdel -r testuser
 # 
 useradd --create-home --comment "Account for running fileshare app" --shell /bin/bash fileshare

python3.7 -m venv testenv


source "testenv/bin/activate"
echo "activated"
pip install -r requirements.txt