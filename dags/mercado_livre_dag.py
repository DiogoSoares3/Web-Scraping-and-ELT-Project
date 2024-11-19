from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, RenderConfig

from include.constants import dbt_path, venv_execution_config
from datawarehouse.sources.utils import verify_data_already_exists, remove_data_from_dir, insert_data_to_postgres

SOURCE_DIR = './datawarehouse/sources/mercado_livre_source'


with DAG(
    "Mercado_livre_DAG",
    schedule_interval="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["mercado_livre"]
) as dag:
    
    with TaskGroup("Data_handling") as data_handling:
        task_1 = PythonOperator(
            task_id="verify_data_already_exists",
            python_callable=verify_data_already_exists,
            op_kwargs={"source_dir": SOURCE_DIR},
            provide_context=True
            )
        task_2 = PythonOperator(
            task_id="insert_data_to_postgres",
            python_callable=insert_data_to_postgres,
            op_kwargs={"schema": "data", "source_dir": SOURCE_DIR},
            provide_context=True
            )
        task_3 = PythonOperator(
            task_id="remove_data_from_dir",
            python_callable=remove_data_from_dir,
            op_kwargs={"data_dir": "{{ ti.xcom_pull(task_ids='insert_data_to_postgres') }}"},
            provide_context=True
            )

        task_1 >> task_2 >> task_3

    run_mercado_livre_crawler = BashOperator(
        task_id="run_mercado_livre_crawler",
        bash_command="{% raw %}cd /usr/local/airflow/datawarehouse/sources/mercado_livre_source/ && sh run_crawlers/mercado_livre_tenis_corrida_masculino.sh{% endraw %}"
    )
    
    insert_data_database = PythonOperator(
        task_id="insert_data_db",
        python_callable=insert_data_to_postgres,
        op_kwargs={"schema": "data", "source_dir": SOURCE_DIR},
        provide_context=True
    )
    
    remove_file = PythonOperator(
        task_id="remove_data_from_data_dir",
        python_callable=remove_data_from_dir,
        op_kwargs={"data_dir": "{{ ti.xcom_pull(task_ids='insert_data_db') }}"},
        provide_context=True
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
            select=["tag:mercado_livre"]
            ),
        execution_config=venv_execution_config,
        default_args={"retries": 3},
    )
    
    data_handling >> run_mercado_livre_crawler >> insert_data_database >> [dbt_tasks, remove_file]
