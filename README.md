## AO3 Web Reader

AO3 web reader / scraper app created using Flask, SQLite, Redis and Bootstrap, supporting:
- Accounts authentication.
- Getting works from ao3.
- Grouping works using tags.
- Auto-update of added works.
- Downloading works.

---

### Production Setup
1. Clone this repo.
2. Generate `.env` config file and change config values (`DB_PATH` and `LOGS_PATH`).
```
python3 generate_dotenv.py
```
3. Run docker container.
```
sudo docker compose up -d
```

### Dev Setup
1. Clone this repo.
2. Generate `.env` config file.
```
python3 generate_dotenv.py
```
3. Change `REDIS_SERVER_ADDRESS` in `.env` to `127.0.0.1`
4. Run DEV docker-compose.
```
sudo docker compose -f docker-compose-dev.yml up
```

### Accounts Management
1. Bash into container.
```
sudo docker container exec -it ao3_web_reader bash
```
2. Run accounts manager cli `python3 users_manager_cli.py`.


### Tests
App contains some example tests for available blueprints. To run them:
```
pytest -v tests/
```


### Scripts
- Fill empty work descriptions:
```
python3 db_scripts/fill_works_descriptions.py
```
