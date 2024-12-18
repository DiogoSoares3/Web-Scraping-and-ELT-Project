#!/bin/bash

docker exec -it api /bin/bash &&
apt update && apt install curl -y &&
curl -s -o /dev/null -w '%{http_code}' http://localhost:8200/api/insert-data-test/
