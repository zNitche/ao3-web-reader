#!/bin/bash

USERNAME=ao3wr
USER_UID=1111
USER_GID=$USER_UID

groupadd --gid $USER_GID $USERNAME
useradd --uid $USER_UID --gid $USER_GID -s /bin/bash -m $USERNAME
