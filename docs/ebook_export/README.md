### Exporting works as HTML

#### Convert html ebook to another formats using Calibre
1. for single file
```
ebook-convert ebook/index.html ebook.azw3
```

2. for many files
```
python3 ebook_convert.py --path /path/to/ebooks/dir
```


#### Calibre Docker setup
run calibre in containerized environment

1. Create core files:

 - Dockerfile
```
FROM ubuntu:jammy
```

 - docker-compose.yml
```
services:
  calibre:
    container_name: calibre-ubuntu
    build: .
    restart: "no"
    volumes:
      - <path_to_your_data_directory>:/home
```

2. build docker image

```
docker compose build
```

3. start + bash into container

```
docker compose run --name calibre calibre bash
```

4. setup calibre

```
sudo apt update
sudo apt install calibre
```

##### Extra

1. bash into already created container

```
docker container start -i <container name, example calibre_run_ba7c7673c2e6>
```

2. disable network access for container

```
docker network disconnect calibre_default <container name, example calibre_run_ba7c7673c2e6>
```
