FROM python:3.9.18-slim

COPY ./app /home/app
WORKDIR /home/app
RUN pip install -r home/file_server/requirements.txt

RUN gunicorn app.py