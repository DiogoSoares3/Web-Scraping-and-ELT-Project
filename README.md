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
