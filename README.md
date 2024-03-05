# A Minimal Flask File Server 
<pre>
|____app
| |____config
| | |____server_config.py
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


### Response to Woven Planet questions
1. Please provide a complete README file that includes following contents:
  a. What is your idea or Ingenuity in design
    I think the ingenuity here is in making this portable and distributable to both users and providers of this as an exposed endpoint. It's not an enterprise quality application and clearly a POC or toy project, but the pieces and tooling are there for someone (me, for instance, but also any other curious engineer) to further build it out, add additional and critical functionality like user storage and authentication, deployment to the public cloud with e.g. S3 for storage and AWS Lambda as the on-demand file server allowing for concurrent requests and indivdualized storage spaces in the cloud, etc. A major issue to note is that the server side secret is hard-coded in the file, and in production, I would certainly externalize that and store it encrypted and securely with an additional process, or in a public service like AWS SMS Parameter Store, and retrieve and renew it regulary as needed.
  b. Instructions on how to build and run (distribute) your code.
    Included in this README file above.
  c. framework and tool / kit information if you use.
    I make use of Flask and gunicorn as my API framework and server, respectively. I built the CLI argument parsing using the standard argparse library in Python. 
  d. Operating system and environment setting information if necessary.
    Nothing in particular is necessary, apart from installation of Python >3.8 as code is platform agnostic, with environment variables provided and read in via Python rather than via e.g. bash or DOS.
3. Make sure your code is well covered by test code to illustrate its robustness.
  Tests are provided, but in all honestly, beginning my career as a data scientist (and then on to data engineering, TDD, and automated SIT as I would like. This portion of the assignment was the most unfamiliar to me, but I made use of ChatGPT on this portion alone to gain at least a basic template from which to learn. 
4. Please zip or tar everything in a directory named yourfirst.lastname/ and return
via email