# Web-Scraping-and-ELT-Project

### First

Configure your `./.env` file based on the `./.env.example` file and your `./datawareshouse/profiles/.env` based on the `./datawareshouse/profiles/.env.example` file.

### Second

Make sure you have the docker engine installed and run:

```
docker compose up -d
```

### Third

To access the PgAdmin4: `localhost:5050`

Then create a new server for this new project. Put the same information that you put in your .env files

### Fourth

To run the DBT commands, you need to be inside the project's container, so put execute this command:

```
docker exec -it dbt bash
```

After that, to ensure that the dbt project is ok, execute

```
dbt debug
```

## Vídeo para entender como o Scrapy e o DBT funcionam

- https://www.youtube.com/live/qNu1VCtUedg?si=k_xIu0CdJrpHj_XV
- https://www.youtube.com/live/n3R0c2ZB6BQ?si=YWN7echIJJb2V4lr