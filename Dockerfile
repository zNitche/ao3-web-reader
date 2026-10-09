# base
FROM python:3.13-slim AS base

RUN apt update && apt -y install curl git

ENV USERNAME=ao3wr
ENV USER_UID=1111
ENV USER_GID=${USER_UID}

RUN groupadd --gid ${USER_GID} ${USERNAME}
RUN useradd --uid ${USER_UID} --gid ${USER_GID} -s /bin/bash -m ${USERNAME}

ENV PY_VENV_DIR="/py_venv"
RUN python3 -m venv "$PY_VENV_DIR"

ENV PATH="${PY_VENV_DIR}/bin:$PATH"

COPY . /ao3_web_reader
WORKDIR /ao3_web_reader

RUN pip3 install -r requirements/requirements.txt
# end

# background_tasks
FROM base AS background_tasks
RUN chmod +x scripts/run_background_tasks.sh
# end

# web_app
FROM base AS web_app
RUN curl -o ao3_web_reader/static/libs/bootstrap.min.css  https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css
RUN curl -o ao3_web_reader/static/libs/bootstrap.bundle.min.js  https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js

RUN pip3 install -r requirements/requirements.txt
RUN pip3 install -r requirements/requirements-prod.txt

RUN chmod +x scripts/entrypoint.sh
# end

# whimdb
FROM base AS whimdb
# end
