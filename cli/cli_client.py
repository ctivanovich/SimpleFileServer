import argparse
import pathlib
import requests
import textwrap
import urllib.parse

from pprint import pprint

from config import sfs_config


# class StoreTrueWithOptionStringAction(argparse.Action):

#     def __init__(self,
#                  option_strings,
#                  dest,
#                  default=None,
#                  required=False,
#                  help=None,
#                  metavar=None):
#         super().__init__(
#         )
    
#     def __call__(self, parser, namespace, values, option_string=None):
#         setattr(namespace, self.dest, self.const)
#         if option_string is not None:
#             setattr(namespace, f'{self.dest}_option_string', option_string)


class SFSSession():
    def __init__(self):
        self.url = f"http://{sfs_config.SERVER}:{sfs_config.PORT}/"
        self.session = requests.Session()
        super().__init__()

    def request_file_list(self):
        try:
            return self.session.request(url=self.url, method = "GET")
        
        except:
            print("FAILED REQUEST: Failure to obtain file list from server.")
    
    def request_upload_file(self, file):
        file_path = pathlib.Path(file)
        file = file_path.stem + file_path.suffix
        
        try:
            return self.session.request(
                url=self.url + urllib.parse.urlencode({"upload": file}),
                files={"file": open(file_path, "rb")},
                method="POST"
            )
        except FileNotFoundError:
            print("File not found. Please ensure file path is full and accurate.")

    def request_delete_file(self, file):
        try:
            return self.session.request(
                url=self.url + urllib.parse.urlencode({"delete": file}),
                method="DELETE"
            )
            
        except FileNotFoundError:
            print(
                "File not found. Make sure to provide the file name exactly \
                as listed after executing the list command."
            )


def main(sfs_session: SFSSession, args: argparse.Namespace)->requests.Response:
    if args.upload:
        resp = sfs_session.request_upload_file(args.upload)
    elif args.delete:
        resp = sfs_session.request_delete_file(args.delete)
    else:
        resp = sfs_session.request_file_list()

    return resp


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
    # action=StoreTrueWithOptionStringAction,
    # const="list",
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
    print(args)
    resp = main(sfs_session, args)
    print(resp.text)