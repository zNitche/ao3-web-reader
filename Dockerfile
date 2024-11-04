FROM python:3.10-slim
#for RaspberryPi
#FROM python:3.10-slim-bullseye

COPY . /ao3_web_reader

WORKDIR /ao3_web_reader

RUN apt update && apt -y install nano curl

RUN curl -o ao3_web_reader/static/libs/bootstrap.min.css  https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css
RUN curl -o ao3_web_reader/static/libs/bootstrap.bundle.min.js  https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js

RUN pip3 install -r requirements/requirements.txt
RUN pip3 install -r requirements/requirements-prod.txt

RUN chmod +x scripts/entrypoint.sh
RUN chmod +x scripts/run_background_task.sh
