# File storage daemon with HTTP API interface


## Requirements

```
Python >= 3.6
Ubuntu >= 18.04

The OS must support systemd, WSL-based systems are not supported. 
```


## How to run

1. Download the repository as zip archive, unzip it

2. Run run.sh script: 
```
./run.sh
```

3. Start the service:
```
systemctl start fs
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
