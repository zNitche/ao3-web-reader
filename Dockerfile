FROM python:3.10.6

COPY . /AO3WebReader

WORKDIR /AO3WebReader

RUN pip3 install -r requirements.txt

CMD gunicorn -c gunicorn.conf.py app:app --preload