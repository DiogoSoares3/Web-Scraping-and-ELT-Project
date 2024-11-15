from datetime import datetime

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, RenderConfig

from include.constants import dbt_path, venv_execution_config
from datawarehouse.sources.insert_data import process_files_in_directory

SOURCES_DIR = './datawarehouse/sources'


with DAG(
    "dbt_profile_overrides_with_taskgroup",
    schedule_interval="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    # tags=["mercado_livre"]
) as dag:
    
    run_puma_crawler = BashOperator(
        task_id="run_puma_crawler",
        bash_command="{% raw %}cd /usr/local/airflow/datawarehouse/sources/puma_source/ && sh run_crawlers/puma_tenis_corrida_masculino.sh{% endraw %}"
    ) ## Arrumar esse path gigante
    
    run_mercado_livre_crawler = BashOperator(
        task_id="run_mercado_livre_crawler",
        bash_command="{% raw %}cd /usr/local/airflow/datawarehouse/sources/mercado_livre_source/ && sh run_crawlers/mercado_livre_tenis_corrida_masculino.sh{% endraw %}"
    ) ## Arrumar esse path gigante
    
    insert_data_database = PythonOperator(
        task_id="insert_data_db",
        python_callable=process_files_in_directory,
        op_kwargs={"schema": "data"},
        provide_context=True  # Permite o uso de kwargs com contexto
    )
    
    dbt_tasks = DbtTaskGroup(
        group_id="DBT",
        project_config=ProjectConfig(dbt_path),
        profile_config=ProfileConfig(
            profile_name="datawarehouse",
            target_name="dev",
            profiles_yml_filepath=dbt_path / "profiles.yml",
        ),
        render_config=RenderConfig(
            emit_datasets=True,
            # select=["tag:mercado_livre"]
            ),
        execution_config=venv_execution_config,
        default_args={"retries": 3},
    )
    
    [run_puma_crawler, run_mercado_livre_crawler] >> insert_data_database >> dbt_tasks
