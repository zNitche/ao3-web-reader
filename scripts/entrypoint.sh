python3 migrate.py

gunicorn -c gunicorn.conf.py app:app --preload