# A Minimal Flask File Server 
<pre>
|____app
| |____config
| | |____server_config.py
| |____Dockerfile
| |____app.py
|____uploads
|____cli
| |____config
| | |____sfs_config.py
| |____cli_client.py
| |____tests
|___|___test.py
|____README
|____requirements.txt
|____.gitignore
</pre>

### File Server

The file server can be built and run exposing port 5000 using the provided Dockerfile with a running Docker application:
```
cd app && docker build -t server .
docker run -p 5000:5000 server
````

If errors around use of the default port emerge, be sure to change the port in the app/config/server_config.py file and then to adjust the docker command accordingly.

If running the server script directly, install the dependencies in requirements.txt, and run with gunicorn from the root directory:
`gunicorn --config ./app/config/server_config.py ./app/app.py:app`

The server exposes the following endpoints:

__/list__ -> print all uploaded files

__/upload=FILE__ -> this will upload files up to 16 MB in size; the maximum size can be increased, and the provided server should be able to handle larger files, up to something reasonable like 256 MB. Max file size is adjustabled in server_config.py.

__/delete=FILE__ -> this will delete the remotely stored <file>, if it exists.

### CLI client

The CLI client is a python app, and its dependencies can be installed running pip install with the provided file:
`pip install -r requirements.txt`. It is advised to first create a virtual environment to avoid conflicts with any base installation you may have.

The configuration in cli/config/cli_config.py can be modified with the correct server address and port if needed.

Supported usage is as follows:
```
python -m cli.cli_client [COMMAND] [FILE]

options:
  -h, --help            show this help message and exit
  --list, -l            Retrieve newline delimited list of existing files.
  --upload UPLOAD, -u UPLOAD
                        Upload file if path/to/file/filename exists locally.
  --delete DELETE, -d DELETE
                        Delete existing file if /path/to/file/filename exists on server.
```

### Testing
With a gunicorn or flask development server running app.py on port 8000, execute cli client tests using pytest (pip install pytest) from within the `cli` client directory.

`python -m pytest tests/tests.py`

Use of python -m pytest is necessary to force pytest to have the root directory imported as a module, which correctly resolves the import hierarchy (see: https://stackoverflow.com/questions/10253826/path-issue-with-pytest-importerror-no-module-named).
