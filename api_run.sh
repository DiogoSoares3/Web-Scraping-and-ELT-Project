#!/bin/bash

echo "Trying to execute test endpoint..."

for i in $(seq 1 30); do
    response=$(curl -s -o /dev/null -w '%{http_code}' http://localhost:8200/api/insert-data-test/)

    response=$(echo "$response" | tr -d '[:space:]')

    echo "HTTP Response: '$response'"

    if [ "$response" -eq 200 ]; then
        echo "API is ready!"
        exit 0
    else
        echo "Attempt $i: HTTP status $response, Waiting for API to be ready..."
        sleep 3
    fi
done

echo "API did not return status code 200 after some attempts."
exit 1