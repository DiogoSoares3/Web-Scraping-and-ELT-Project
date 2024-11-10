#!/bin/bash

docker compose -f docker-compose-dbt.yaml up --build -d
docker exec -it dbt bash