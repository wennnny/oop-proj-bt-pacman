#!/usr/bin/env bash

NAME=aoop
REPOSITORY="argnctu/oop"
TAG="ros-unity"
REPO_NAME=oop-proj-bt-pacman

IMG="${REPOSITORY}:${TAG}"

xhost +
containerid=$(docker ps -aqf "ancestor=${IMG}") && echo "$containerid"
docker exec -it \
    --privileged \
    -e DISPLAY="${DISPLAY}" \
    -e LINES="$(tput lines)" \
    "${containerid}" \
    bash
xhost -
