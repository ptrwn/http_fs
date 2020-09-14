# File storage daemon with HTTP API interface

## How to run

1. Set up virtual enviroment for the app:
```
# create
$ python -m venv <env_name>

# activate
$ source <env_name>/bin/activate

# install dependencies
$ pip install -r requirements.txt
```

2. Set up daemon to run it:

For Ubuntu on HW or in VM
```
# update config file:
fs.service

# put the config file into /etc/systemd/system

# restart systemd so that it sees the new unit
$ sudo systemctl daemon-reload

# interact with the app like with any other service
$ sudo systemctl start fs
$ sudo systemctl stop fs
$ sudo systemctl restart fs
$ sudo systemctl status fs
```


For Ubuntu in WSL (or anywhere else with no systemd out of the box)
```
# install supervisor:
$ sudo apt install supervisor

# update /etc/supervisor/supervisord.conf with
[program:fs]
command=<full path to virtual environment>/venv/bin/gunicorn -b localhost:4000 -w 2 app:app
directory=<path to project folder>
autostart=true
autorestart=true
stderr_logfile=/var/log/fs.err.log
stdout_logfile=/var/log/fs.out.log

# reload supervisord with updated config
$ supervisord -c supervisord.conf

#start the application
$ supervisorctl start fs

```


## How to use

1. Upload a new file
```
$ curl -X POST 127.0.0.1:4000/api/upload -F 'file=@<path/to/file>' -i
```

2. Download a file from file share
```
$ curl 127.0.0.1:4000/api/file/<file hash> --output some.file
```

3. Delete a file from file share. If after file removal no other files were left in the subfolder, it will be deleted too
```
$ curl -X DELETE 127.0.0.1:4000/api/file/<file hash>
```
