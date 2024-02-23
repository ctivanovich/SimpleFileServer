# Simple File Server
<pre>
|____app
| |____config
| | |____gunicorn_config.py
| |____Dockerfile
| |____app.py
|____tests
|______tests.py
|____uploads
|____cli
| |____config
| | |____sfs_config.py
| |____cli_client.py
|____README
|____setup.py
|____.gitignore
</pre>

### File Server

The file server can be built and run exposing port 8000 using the provided Dockerfile:
```
cd app && docker build -t server .
docker run -p 8000:8000 server
````

If running the server script directly, install the dependencies in requirements.txt, and run with gunicorn:

`gunicorn --config ./app/config/gunicorn_config.py ./app/app.py`

The server exposes the following endpoints:

__/list__ -> print all uploaded files


__/upload=FILE__ -> this will upload files up to 16mb in size; the maximum size can be increased, and the providedå server should be able to handle larger files.


__/delete=FILE__ -> this will delete the remotely stored <file>


### CLI client

The CLI client is a python app, and its dependencies can be installed running the provided setup.py file:
python setup.py

The configuration in cli/config/sfs_config.py can be modified with the correct server address and port if needed.

Supported usage is as follows:
```
python cli_client.py [COMMAND] [FILE]

options:
  -h, --help            show this help message and exit
  --list, -l            Retrieve newline delimited list of existing files.
  --upload UPLOAD, -u UPLOAD
                        Upload file if path/to/file/filename exists locally.
  --delete DELETE, -d DELETE
                        Delete existing file if /path/to/file/filename exists on server.
```