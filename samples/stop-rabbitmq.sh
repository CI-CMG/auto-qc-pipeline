#!/bin/bash

set -ex

docker container stop rabbitmq-1
docker container rm rabbitmq-1