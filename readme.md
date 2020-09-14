# File storage daemon with HTTP API interface

## How to run

1. Set up virtual enviroment for the app:
```
# create
python -m venv <env_name>

# activate
source <env_name>/bin/activate

# install dependencies
pip install -r requirements.txt
```

2. Set up daemon to run it:

For Ubuntu on HW or in VM
```
# update config file:
fs.service

# put the config file into /etc/systemd/system

# restart systemd so that it sees the new unit
sudo systemctl daemon-reload

$ sudo systemctl start fs
$ sudo systemctl stop fs
$ sudo systemctl restart fs
$ sudo systemctl status fs
```


For Ubuntu in WSL (or anywhere else with no systemd out of the box)
```
# install supervisor:
sudo apt install supervisor

# update /etc/supervisor/supervisord.conf with
[program:fs]
command=<full path to virtual environment>/venv/bin/gunicorn -b localhost:4000 -w 2 app:app
directory=<path to project folder>
autostart=true
autorestart=true
stderr_logfile=/var/log/fs.err.log
stdout_logfile=/var/log/fs.out.log

# reload supervisord with updated config
supervisord -c supervisord.conf

#start the application
supervisorctl start fs

```