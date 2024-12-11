# Web-Scraping-and-ELT-Project

## Introduction

This project implements a ELT (Extract, Load, Transform) data engineer logic. It implements a web scraping and data pipeline solution to analyze men's running shoes data from multiple online platforms, including Puma Oficial Website, Magazine Luiza, and Mercado Livre. It adopts the Medallion Architecture to structure the data pipeline into Bronze (raw), Silver (staging), and Gold (datamart) layers, enabling efficient data processing, transformation, and enrichment.

The primary objectives of this project are:

- Data Automation: Automate the process of scraping product data from websites.
- Data Structuring: Organize scraped data into distinct layers (raw, processed, and enriched) for better usability and organization. This can be util for Data Engineers, Data Scientists and Data Analysts.
- Insights Generation: Derive actionable insights, such as identifying the top 10 best-priced shoes and monitoring price changes over time.
- User-Friendly Interaction: Integrate with Telegram Bot and Streamlit for enhanced user experience, including notifications and visual dashboards.

The pipeline is orchestrated using Apache Airflow, Astro CLI and Cosmos, with separate DAGs handling data collection, transformation, and enrichment. Key technologies like Scrapy (for scraping), DBT (for transformation), and Python APIs ensure seamless integration and performance.
Pipeline Overview

The pipeline consists of the following stages, visualized in the attached DAG flow diagram:

1. Data Handling:
    - Verify Data: Ensure if already exists JSON data extracted by an old crawler that was not inserted in the database.
    - Insert to PostgreSQL: Store raw scraped data in the Bronze layer.
    - Cleanup: Remove temporary files after ingestion.

2. Run Crawlers:
    - Separate BashOperators handle scraping for Puma Website, Magazine Luiza, and Mercado Livre. The can run in parallel
    - Data from all sources is integrated into a PostgreSQL database, more specific in the raw tables.

3. DBT Transformations:
    - Staging tables (stg-*) clean, standardize and eliminate duplicated records in the raw data.
    - Gold-layer views like price_over_time_infusion, metrics_puma_prices and top10_best_puma_shoes_price provide enriched insights of Puma running shoes.

4. Notifications:
    - A Telegram Bot sends alerts based on key metrics of the price_over_time_infusion, such as significant price drops, availability of top-priced and the price over time of the Infusion Puma sneaker.

5. Graphical Interface
    - A Streamlit App for data visualization using the golden layer data to aggregate information to a decision maker of the business area.

### Main Tecnologies used

![alt text](images/image.png)

The Project is executed using the Astronomer Apache Airflow using the Astro CLI and Cosmos. This is a good solution to people trying to run a DBT project with Airflow.

- Apache Airflow: Orchestrates the pipeline's execution, ensuring tasks are run in sequence and dependencies are respected. Also a powerful tool for scheduling the pipeline exetution.
- Scrapy: Handles web scraping for extracting product data from e-commerce websites.
- PostgreSQL: Serves as the data warehouse, storing raw (Bronze), processed (Silver), and enriched (Gold) data layers.
- DBT (Data Build Tool): Performs SQL-based data transformations to clean, structure, and enrich the data.
- Telegram Bot: Provides user notifications about insights and alerts, such as price updates or best deals.
- Docker: Ensures an isolated and consistent environment for running all pipeline components in containers.
- FastAPI: A Python Framework to build robust APIs.
- Streamlit: A Python lib for data visualization.

### The Project's Tree

Where is the project's tree for a better undertanding of how the content is structured:

```bash
.
├── api
│   ├── core
│   │   ├── configs.py
│   │   ├── database.py
│   │   ├── deps.py
│   │   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   ├── __all_models.py
│   │   ├── infusion_model.py
│   │   ├── metrics_model.py
│   │   └── top10_puma_model.py
│   ├── requirements.txt
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── puma_shoes_schema.py
│   └── src
│       ├── database_operations.py
│       ├── __init__.py
│       ├── puma_shoes.py
│       └── telegram_connections.py
├── app
│   ├── __init__.py
│   └── ui
│       ├── assets
│       ├── home.py
│       ├── __init__.py
│       ├── pages
│       │   ├── __init__.py
│       │   ├── metrics_puma.py
│       │   └── top10_best_puma.py
│       └── utils
│           ├── api_calls.py
│           ├── __init__.py
├── dags
│   ├── all_data_dag.py
│   ├── magalu_dag.py
│   ├── mercado_livre_dag.py
│   ├── puma_site_dag.py
├── datawarehouse
│   ├── dbt_project.yml
│   ├── docs
│   ├── __init__.py
│   ├── logs
│   │   └── dbt.log
│   ├── models
│   │   ├── gold
│   │   │   ├── metrics_puma_prices.sql
│   │   │   ├── price_over_time_infusion.sql
│   │   │   ├── schema.yml
│   │   │   └── top10_best_puma_shoes_price.sql
│   │   ├── schema.yml
│   │   └── silver
│   │       ├── schema.yml
│   │       ├── stg-magalu_tenis_corrida_masculino.sql
│   │       ├── stg-mercado_livre_tenis_corrida_masculino.sql
│   │       └── stg-puma_tenis_corrida_masculino.sql
│   ├── profiles.yml
│   ├── README.md
│   ├── seeds
│   ├── sources
│   │   ├── __init__.py
│   │   ├── magalu_source
│   │   │   ├── backup
│   │   │   │   └── magalu_tenis_corrida_masculino.json
│   │   │   ├── data
│   │   │   │   └── magalu_tenis_corrida_masculino.json
│   │   │   ├── magalu_source
│   │   │   │   ├── __init__.py
│   │   │   │   ├── middlewares.py
│   │   │   │   ├── settings.py
│   │   │   │   └── spiders
│   │   │   │       ├── __init__.py
│   │   │   │       ├── magalu_tenis_corrida_masculino.py
│   │   │   ├── run_crawlers
│   │   │   │   └── magalu_tenis_corrida_masculino.sh
│   │   │   └── scrapy.cfg
│   │   ├── mercado_livre_source
│   │   │   ├── backup
│   │   │   │   └── mercado_livre_tenis_corrida_masculino.json
│   │   │   ├── data
│   │   │   │   └── mercado_livre_tenis_corrida_masculino.json
│   │   │   ├── mercado_livre_source
│   │   │   │   ├── __init__.py
│   │   │   │   ├── middlewares.py
│   │   │   │   ├── settings.py
│   │   │   │   └── spiders
│   │   │   │       ├── __init__.py
│   │   │   │       ├── mercado_livre_tenis_corrida_masculino.py
│   │   │   ├── run_crawlers
│   │   │   │   └── mercado_livre_tenis_corrida_masculino.sh
│   │   │   └── scrapy.cfg
│   │   ├── puma_source
│   │   │   ├── backup
│   │   │   │   └── puma_tenis_corrida_masculino.json
│   │   │   ├── data
│   │   │   │   └── puma_tenis_corrida_masculino.json
│   │   │   ├── puma_source
│   │   │   │   ├── __init__.py
│   │   │   │   ├── settings.py
│   │   │   │   └── spiders
│   │   │   │       ├── __init__.py
│   │   │   │       ├── puma_tenis_corrida_masculino.py
│   │   │   ├── run_crawlers
│   │   │   │   └── puma_tenis_corrida_masculino.sh
│   │   │   └── scrapy.cfg
│   │   └── utils.py
├── docker
│   ├── dbt-requirements.txt
│   ├── docker-compose-dbt.yaml
│   ├── Dockerfile.api_app
│   ├── Dockerfile.dbt
│   └── execute.sh
├── docker-compose.override.yml
├── Dockerfile
├── down_no_airflow.sh
├── down.sh
├── include
│   ├── constants.py
│   ├── profiles.py
│   └── __pycache__
│       ├── constants.cpython-312.pyc
│       └── telegram_connection.cpython-312.pyc
├── logs
│   └── dbt.log
├── packages.txt
├── plugins
├── README.md
├── requirements.txt
├── start_no_airflow.sh
├── start.sh
├── tests
│   └── dags
│       └── test_dag_integrity.py
```

### Main directories descripton

- We can see that we have an `api` directory, where our FastAPI Api will be configured to return data from the golden layer for our aplications, such as the Telegram Alert Bot and the Streamlit app.

- The `app` directory host the Streamlit App for data visualisation

- The `dags` directory contains the Airflow DAGs that will be executed for running

- The `datawarehouse` directory contains all of the project's business logic. It contains the sub-directory `datawarehouse/sources`, which contains all the Scrapy crawlers code. It also contains the sub-directory `datawarehouse/sources`, which contains all the Medallion Architecture, with the Bronze, Silver and Gold layers containing SQL scripts for the DBT execution.

- A `docker` directory for to help handling the Dockerfiles, requeirements.txt files and bash scripts to run in the project context.

## Project Workflow and Implementation

The project is designed following the Medallion Architecture, leveraging a multi-layered data processing approach to extract, transform, and analyze male running shoes' product data from three sources: Magazine Luiza, Mercado Livre, and the official Puma website. The pipeline is structured into three key data layers: Bronze, Silver, and Gold, with a FastAPI-based API, a Streamlit front-end for visualization and a Telegram Bot for price alerts.

### Data Collection and Bronze Layer

The process begins with three Scrapy crawlers, each designed to scrape product data in JSON format from the respective e-commerce platforms. These JSON files are inserted directly into a PostgreSQL database as raw tables, forming the Bronze Layer. The focus here is on ingesting raw data without preprocessing, ensuring all retrieved information is stored for traceability.

### Silver Layer: Data Cleaning and Transformation

The Silver Layer processes the raw data using DBT (Data Build Tool). SQL scripts are executed to:

- Eliminate duplicate records.
- Normalize attribute formats (e.g., standardizing date, currency, or text formats).
- Perform data type transformations.

The result of these transformations is a set of staging tables, which clean and structure the data for further analysis.

### Gold Layer: Business-Enriched Data

The Gold Layer applies business logic to the structured data from the Silver Layer. This is achieved through DBT views, which:

- Perform statistical analyses and data aggregation.
- Execute complex queries to cross-reference data across sources.
- Create enriched datasets tailored to specific business needs.

These business logics produced the following views:

- `metrics_puma_prices`:
    - A view that shows a bunch of Statistics metrics related to Puma shoes along all the websites.

- `price_over_time_infusion`:
    - A View that shows the Price of the Infusion Puma shoes over time in Mercado Livre, Magazine Luiza and Puma website sources.

- `top10_best_puma_shoes_price`:
    - A View that shows the Top 10 best Puma shoes price of all the websites combined.

These views automate tasks typically handled by data analysts or data scientists, providing ready-to-use insights to a decision maker.

### Apache Airflow as an Orchestrator

![alt text](images/image-2.png)

Apache Airflow is a strategic and effective choice for orchestration in a Medallion Architecture, particularly due to its flexibility and ability to handle complex dependencies across multiple data processing layers.

In the Bronze Layer, which deals with raw data, Airflow plays a key role in scheduling crawlers to collect data from external sources such as Magazine Luiza, Mercado Livre, and Puma Webiste. By automating this process, the pipeline ensures consistent and regular data collection. The schedule can also be optimized to reduce the load on external servers while guaranteeing that the data remains up-to-date.

The Silver Layer, responsible for cleaning and validating the data, relies on Airflow to manage dependencies between tasks. For example, once the raw data has been ingested into the Bronze Layer, Airflow triggers validation scripts to remove duplicates and format the data for further analysis. This ensures that only high-quality, structured data moves forward in the pipeline.

In the Gold Layer, business rules are applied to generate actionable insights. Airflow orchestrates the execution of SQL transformations managed by DBT, ensuring that insights are derived from the cleaned and enriched data. By automating this flow, Airflow guarantees a consistent transformation process and delivers high-quality datasets ready for use.

A critical feature of this pipeline is the integration of Airflow with a Telegram bot for alerts. At the end of the process, the bot notifies stakeholders about significant updates, such as price changes in the Gold Layer. This automation provides several benefits:

- Instant insights: Teams are notified in real time, enabling quicker decision-making.
- Proactivity: Alerts allow stakeholders to adjust strategies promptly, such as revising purchasing or pricing decisions.
- Efficiency: Automated alerts eliminate the need for manual checks on pipelines or dashboards.

In summary, this pipeline offers several advantages, such as:

- Modularity: The clear separation between the Bronze, Silver, and Gold Layers ensures flexibility and ease of maintenance.
- Scalability: Airflow handles parallel tasks efficiently, enabling the pipeline to run multiple crawler in just one DAG.
- Complete monitoring: The Airflow dashboard provides real-time visibility into each step of the process, making it easy to identify bottlenecks or failures.
- End-to-end automation: From data collection to final alerts, the process is fully automated, minimizing manual intervention and human error.

### Integration with FastAPI and Streamlit

After the data has passed through the Gold Layer, the API and the Streamlit App are ready for use.

1. A FastAPI-based API is used to query the enriched views. This API serves as the backbone for integrating the processed data with other services or applications.

    ![alt text](images/image-1.png)

2. A Streamlit front-end consumes this API to visualize the data through interactive charts and tables. Each Gold Layer view corresponds to a specific business area, ensuring that insights are categorized and actionable.

- The view `metrics_puma_prices` represented in a Streamlit enpoint as business area:

    ![alt text](images/image-3.png)

- The view `top10_best_puma_shoes_price` represented in a Streamlit enpoint as an another business area:

    ![alt text](images/image-4.png)


### Telegram Bot Integration

As part of the Airflow pipeline execution, once the DBT scripts complete, a FastAPI endpoint queries the enriched view `price_over_time_infusion`, and then a Telegram Bot sends real-time alert to the users that signed this bot, notifying them about important events and insights based on this golden layer view `price_over_time_infusion`.

![alt text](images/image-5.png)

This end-to-end pipeline from data extraction to enriched data visualization—provides a robust solution for automating the processing and analysis of e-commerce product data, reducing manual effort and enhancing decision-making processes.

## How to Run the Project


### Enviroment configs


## Conclusion and Next Steps
