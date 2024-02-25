import pytest
from unittest.mock import MagicMock, patch
from cli.cli_client import SFSSession, main

@pytest.fixture
def mock_session():
    return SFSSession()

def test_request_file_list_success(mock_session):
    mock_session.session.request = MagicMock(return_value=MagicMock(text="file1\nfile2\nfile3"))
    response = mock_session.request_file_list()
    assert response.text == "file1\nfile2\nfile3"

def test_request_file_list_failure(mock_session):
    mock_session.session.request = MagicMock(side_effect=requests.exceptions.RequestException)
    response = mock_session.request_file_list()
    assert response.status_code == 404
    assert response.text == "FAILED REQUEST: Failure to obtain file list from server."

def test_request_upload_file_success(mock_session):
    with patch("builtins.open", return_value=MagicMock()) as mock_open:
        mock_session.session.request = MagicMock(return_value=MagicMock(text="Upload successful."))
        response = mock_session.request_upload_file("test.txt")
        assert response.text == "Upload successful."
        mock_open.assert_called_once_with("test.txt", "rb")

def test_request_upload_file_file_not_found(mock_session):
    response = mock_session.request_upload_file("nonexistent.txt")
    assert response.status_code == 404
    assert response.text == "File not found. Please ensure file path is full and accurate."

def test_request_delete_file_success(mock_session):
    mock_session.session.request = MagicMock(return_value=MagicMock(text="Deletion successful."))
    response = mock_session.request_delete_file("test.txt")
    assert response.text == "Deletion successful."

def test_request_delete_file_file_not_found(mock_session):
    response = mock_session.request_delete_file("nonexistent.txt")
    assert response.status_code == 404
    assert response.text == "File not found. Make sure to provide the file name exactly as listed after executing the list command."

def test_main_upload(mock_session):
    mock_session.request_upload_file = MagicMock(return_value=MagicMock(text="Upload successful."))
    args = MagicMock(upload="test.txt", delete=None, list=None)
    response = main(mock_session, args)
    assert response.text == "Upload successful."

def test_main_delete(mock_session):
    mock_session.request_delete_file = MagicMock(return_value=MagicMock(text="Deletion successful."))
    args = MagicMock(upload=None, delete="test.txt", list=None)
    response = main(mock_session, args)
    assert response.text == "Deletion successful."

def test_main_list(mock_session):
    mock_session.request_file_list = MagicMock(return_value=MagicMock(text="file1\nfile2\nfile3"))
    args = MagicMock(upload=None, delete=None, list=True)
    response = main(mock_session, args)
    assert response.text == "file1\nfile2\nfile3"

def test_main_exception(mock_session, capsys):
    mock_session.request_file_list = MagicMock(side_effect=Exception("Test Exception"))
    args = MagicMock(upload=None, delete=None, list=True)
    response = main(mock_session, args)
    captured = capsys.readouterr()
    assert captured.out == "Unhandled Exception, please contact maintainers: Test Exception\n"
