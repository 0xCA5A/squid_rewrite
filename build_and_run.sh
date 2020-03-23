#!/bin/bash

CONTAINER_NAME=squid_rewrite
IMAGE_NAME=${CONTAINER_NAME}:latest

if [[  $# -ne 1  ]] || [[ ! -f $1  ]]; then
    echo "[!] Need an absolute path to an existing Squid config file"
    echo -e "\t$ ./build_and_run.sh \$(pwd)/squid_rewrite.conf"
    exit 1
fi

echo "[i] Kill / remove old container if present"
ID=$(docker ps -a | grep ${CONTAINER_NAME} | cut -d ' ' -f 1); echo "$ID"; docker kill "$ID"; docker rm "$ID"

echo "[i] Build the Squid proxy container"
cd docker; docker build -t ${CONTAINER_NAME} -f Dockerfile . ; cd -

echo "[i] Run the Squid proxy container"
docker run --name ${CONTAINER_NAME} --detach=false --restart=always \
  --publish 3128:3128 \
  --volume "${1}":/etc/squid/squid.conf \
  ${IMAGE_NAME}
