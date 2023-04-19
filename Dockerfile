FROM python:3.10-slim
#FROM python:3.10-slim-bullseye for RaspberryPi

COPY . /AO3WebReader

WORKDIR /AO3WebReader

RUN apt update && apt -y install nano curl

RUN curl -o ao3_web_reader/static/libs/bootstrap.min.css  https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css
RUN curl -o ao3_web_reader/static/libs/bootstrap.bundle.min.js  https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js

RUN pip3 install -r requirements.txt

CMD gunicorn -c gunicorn.conf.py app:app --preload