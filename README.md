## AO3 Web Reader

AO3 web reader / scraper app created using Flask, SQLite, Redis and Bootstrap, supporting:
- Accounts authentication.
- Getting works from ao3.
- Grouping works using tags.
- Auto-update of added works.
- Downloading works.

---

Django reimplementation [here](https://github.com/zNitche/ao3-web-reader-django)

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


### Migrations Scripts
Scripts used to keep database data compatible with app new releases

- Fill empty work descriptions:
```
python3 migrations_stripts/fill_works_descriptions.py
```

- Convert old database (with TextRows) to new one (post commit: `5b1385d5b15e75f527fa88f95a6a1dfb00cbd8e4`):
  1. generate database json file:
    ```
    python3 migrations_stripts/dump_db_data.py --old_db_path "old_db_path" \
                                               --output_path "data_output_path" \
                                               --models-path "scripts.legacy_db_post_5b1385d.legacy_models" \
                                               --models User UpdateMessage Work Tag Chapter TextRow
    ```
  2. create new database
    ```
    python3 app.py
    ```
  3. fill database with dumped data:
    ```
    python3 migrations_stripts/create_new_db_from_data_post_5b1385d.py --new_db_path "new_db_path" --db_data_path "dumped_data_path"
    ```
  

- Convert old database (without chapter ids, chapter order id and update message type) to new one (post commit: `f2e40e5`):
  1. generate database json file:
    ```
    python3 migrations_stripts/dump_db_data.py --old_db_path "old_db_path" \
                                               --output_path "data_output_path" \
                                               --models-path "scripts.legacy_db_post_f2e40e5.legacy_models" \
                                               --models User UpdateMessage Work Tag Chapter
    ```
  2. create new database
    ```
    python3 app.py
    ```
  3. fill database with dumped data:
    ```
    python3 migrations_stripts/create_new_db_from_data_post_f2e40e5.py --new_db_path "new_db_path" --db_data_path "dumped_data_path"
    ```
