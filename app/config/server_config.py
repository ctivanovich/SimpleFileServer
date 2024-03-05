import os

FLASK_MAX_FILE_SIZE = 16 * 1000 * 1000  ## 16 mb
workers = int(os.environ.get('GUNICORN_PROCESSES', '2'))
threads = int(os.environ.get('GUNICORN_THREADS', '4'))
timeout = int(os.environ.get('GUNICORN_TIMEOUT', '300'))
bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8000')
forwarded_allow_ips = '*'
secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }