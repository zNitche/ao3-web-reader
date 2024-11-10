## AO3 Web Reader

AO3 web reader / scraper app created using Flask, SQLite, Redis and Bootstrap, supporting:
- Accounts authentication.
- Getting works from AO3.
- Grouping works using tags.
- Adding works to favorites.
- Auto-update of added works.
- Downloading works.
- Force updating chapters.


### Production Setup
1. Clone this repo.
2. Create `.env` config file and change config values (`DB_PATH` and `LOGS_PATH`).
```
cp .env.template .env
```
3. Run docker container.
```
sudo docker compose up -d
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
sudo docker compose -f docker-compose-dev.yml up
```


### Database Migrations
```
python3 migrate.py
```


### Accounts Management
1. Bash into container.
```
sudo docker container exec -it ao3_web_reader bash
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
