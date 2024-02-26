import argparse
import pathlib
import requests
import textwrap
import urllib.parse

from io import BytesIO
from typing import Union, Tuple
from requests.models import Response

from config.cli_config import SERVER, PORT


class SFSSession:
    def __init__(self):
        self.url = f"http://{SERVER}:{PORT}/"
        self.session = requests.Session()
        self.client_side_generic_response = Response()

    def request_file_list(self) -> str | Response:
        try:
            return self.session.request(url=self.url, method="GET")

        except:
            self.client_side_generic_response.raw = BytesIO(b"FAILED REQUEST: Failure to obtain file list from server.")
            self.client_side_generic_response.status_code = 404
            return self.client_side_generic_response

    def request_upload_file(self, file) -> str | Response:
        file_path = pathlib.Path(file)
        file = file_path.stem + file_path.suffix

        try:
            return self.session.request(
                url=self.url + urllib.parse.urlencode({"upload": file}),
                files={"file": open(file_path, "rb")},
                method="POST",
            )
        except FileNotFoundError:
            self.client_side_generic_response.raw = BytesIO(b"File not found. Please ensure file path is full and accurate.")
            self.client_side_generic_response.status_code = 404
            return self.client_side_generic_response

    def request_delete_file(self, file) -> str | Response:
        try:
            return self.session.request(
                url=self.url + urllib.parse.urlencode({"delete": file}), method="DELETE"
            )

        except:
            self.client_side_generic_response.raw = BytesIO(b"Server side failure. Make sure to provide the file name exactly \
            as listed after executing the list command.")
            self.client_side_generic_response.status_code = 404
            return self.client_side_generic_response


def main(sfs_session: SFSSession, args: argparse.Namespace) -> str:
    try:
        if args.upload:
            resp = sfs_session.request_upload_file(args.upload)
        elif args.delete:
            resp = sfs_session.request_delete_file(args.delete)
        else:
            resp = sfs_session.request_file_list()

        return resp

    except Exception as e:
         return f"Unhandled Exception, please contact maintainers: {e}"
        


parser = argparse.ArgumentParser(
    prog="SimpleFileServer",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
        """\
        A friendly client for interacting with your remote file server.\n
        Requires installation of Python and dependencies in requirements.txt.
        Usage:
            python cli_client.py [COMMAND] [FILE]
        """
    ),
)

parser.add_argument(
    "--list",
    "-l",
    action="store_true",
    dest="list",
    help="Retrieve newline delimited list of existing files.",
)
parser.add_argument(
    "--upload",
    "-u",
    dest="upload",
    action="store",
    help="Upload file if path/to/file/filename exists locally.",
)
parser.add_argument(
    "--delete",
    "-d",
    dest="delete",
    action="store",
    help="Delete existing file if /path/to/file/filename exists on server.",
)

if __name__ == "__main__":
    args = parser.parse_args()
    sfs_session = SFSSession()
    resp = main(sfs_session, args)
    print(resp.text)
