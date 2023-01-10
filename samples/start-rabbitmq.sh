#!/bin/bash

set -ex

docker run -d --network skynet --name rabbitmq-1 -p 15672:15672 -p 5672:5672 rabbitmq:management-alpine