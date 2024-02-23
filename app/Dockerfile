FROM python:3.10

VOLUME [ "/data/uploads" ]

WORKDIR /home/app
COPY . /home/app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000 5000

CMD ["gunicorn","--config", "config/gunicorn_config.py", "app:app"]