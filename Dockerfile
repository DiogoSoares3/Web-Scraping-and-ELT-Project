FROM quay.io/astronomer/astro-runtime:12.1.1

# install dbt into a virtual environment
RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-postgres==1.8.2 && deactivate

RUN chmod -R 775 /usr/local/airflow/datawarehouse/sources

# set a connection to the airflow metadata db to use for testing
ENV AIRFLOW_CONN_AIRFLOW_METADATA_DB=postgresql+psycopg2://postgres:postgres@postgres:5432/WebScraping?options=-csearch_path%public
