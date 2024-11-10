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



# Para criar novo projeto de Crawler:

Primeiro entre na camada bronze:

```bash
cd ./datawarehouse/models/bronze/
```

Depois execute o comando do Scrapy para iniciar o projeto:

```bash
scrapy startproject <nome da fonte de dados>
```

Depois entre na pasta que o scrapy criou:

```bash
cd ./<nome da fonte de dados>
```

E execute o seguinte comando para referenciar o site a qual você quer fazer o crawler:

```bash
scrapy genspider <nome do spider> <url>
```

Entre no diretorio onde foi criado os arquivos de configuração do projeto:

```bash
cd <nome da fonte de dados>
```

E execute:

```bash
scrapy shell
```

O comando acima deve ser executado no mesmo diretorio onde contem o arquivo `setting.py`, pois é onde se tem as configurações de User-agent.

### Para executar o script do spider com o parser:

```bash
scrapy crawl <variavel 'name' dentro da classe do spider> -o <path/output>.json
```