#!/bin/bash

set -xe

docker build -t vv1sp/postgres-dummy-writer:latest .
docker push vv1sp/postgres-dummy-writer:latest
