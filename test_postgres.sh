echo "Waiting for PostgreSQL to be ready..."

for i in $(seq 1 30);
do
    docker exec db pg_isready -h localhost -p 5432 > /dev/null 2>&1

    if [ $? -eq 0 ]; then
    echo "PostgreSQL is ready!"
    exit 0
    fi

    echo "Attempt $i: PostgreSQL is not ready yet. Retrying in 3 seconds..."
    sleep 3
done

echo "Error: PostgreSQL did not become ready after 30 attempts."
exit 1