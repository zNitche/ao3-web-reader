## AO3 Web Reader

AO3 web reader / scraper app created using Flask, SQLite, Redis and Bootstrap, supporting:
- Accounts authentication.
- Getting works from AO3.
- Grouping works using tags.
- Adding works to favorites.
- Auto-update of added works.
- Downloading works.
- Force updating chapters, works and tags.
- Exporting works for ebook readers (html format), read [this](docs/ebook_export/README.md).


Hello there, It's been almost 2 years since I started working on this project, a lot of time right?

Anyway since then I became much better programmer, and despite that this project works pretty good 
I decided that it is time for major refactoring which will ensure easier maintenance further down the road.

And here we are, below you can find a list of things that have been done.

1. Complete dependencies overhaul and proper fragmentation.
2. Alembic based database migrations.
3. Database reimplementation (replaced Flask-SQLAlchemy with sqlalchemy) + custom pagination
(since sqlalchemy doesn't support page base pagination).
4. New session based authentication system (removed Flask-Login).
5. Background tasks refactoring (dev mode app auto reloading finally works).
6. Proper logging implementation.
7. Styling tweaks + UI bugfixes.
8. Internal app data flow refactoring, to improve readability.
9. Improved Docker services architecture.


### Production Setup
1. Clone this repo (for stable experiance switch to one of the release tags).
2. Create `.env` config file and change config values (`DB_PATH` and `LOGS_PATH`).
```
cp .env.template .env
```
3. (Optional) Enable HTTPS, generate new certificates, or provide your own
```
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```
4. Run docker container.
```
docker compose up -d
```

### Dev Setup
1. Clone this repo.
2. Generate `.env` config file.
```
cp .env.template .env
```
3. Change `REDIS_SERVER_ADDRESS` in `.env` to `127.0.0.1`
4. Install development dependencies 
```
pip3 install -r requirements/requirements-dev.txt
```
5. Run DEV docker-compose.
```
docker compose -f docker-compose-dev.yml up
```


### Database Migrations
```
python3 migrate.py
```


### Accounts Management
1. Bash into container.
```
docker container exec -it ao3_web_reader bash
```
2. Run accounts manager cli `python3 users_manager_cli.py`.


### Tests
App contains some example tests for available routes. To run them:
```
pytest -v tests/
```


### Extras
Back when I was learning Django I created this repo [reimplementation](https://github.com/zNitche/ao3-web-reader-django).

Keep in mind that it hasn't been updated since it was finished and might not work anymore.
