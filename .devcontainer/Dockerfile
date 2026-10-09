FROM python:3.13

ARG USERNAME=ao3_web_reader_worker
ARG USER_UID=1111
ARG USER_GID=${USER_UID}

# Add non root user
RUN groupadd --gid ${USER_GID} ${USERNAME}
RUN useradd --uid ${USER_UID} --gid ${USER_GID} -s /bin/bash -m ${USERNAME}

# Container setup
RUN apt update && apt install -y git wget

# Setup container user
USER ${USERNAME}

# Done
ENTRYPOINT [ "/bin/bash" ]