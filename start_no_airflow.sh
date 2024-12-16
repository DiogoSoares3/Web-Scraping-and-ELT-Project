#!/bin/bash

docker compose -f docker/docker-compose-dbt.yaml up --build -d
docker exec -it dbt-container bash