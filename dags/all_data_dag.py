from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, RenderConfig

from include.constants import dbt_path, venv_execution_config
from datawarehouse.sources.utils import verify_data_already_exists, remove_data_from_dir, insert_data_to_postgres

SOURCE_DIR = './datawarehouse/sources'


with DAG(
    "All_data_DAG",
    schedule_interval="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False
) as dag:
    
    with TaskGroup("Data_handling") as data_handling:

        task_1 = PythonOperator(
            task_id="verify_data_already_exists",
            python_callable=verify_data_already_exists,
            )
        task_2 = PythonOperator(
            task_id="insert_data_to_postgres",
            python_callable=insert_data_to_postgres,
            )
        task_3 = PythonOperator(
            task_id="remove_data_from_dir",
            python_callable=remove_data_from_dir,
            )

        task_1 >> task_2 >> task_3
        
    with TaskGroup("Run_crawlers") as run_crawlers:
        
        run_puma_crawler = BashOperator(
            task_id="run_puma_crawler",
            bash_command="{% raw %}cd /usr/local/airflow/datawarehouse/sources/puma_source/ && sh run_crawlers/puma_tenis_corrida_masculino.sh{% endraw %}"
        ) ## Arrumar esse path gigante
        
        run_mercado_livre_crawler = BashOperator(
            task_id="run_mercado_livre_crawler",
            bash_command="{% raw %}cd /usr/local/airflow/datawarehouse/sources/mercado_livre_source/ && sh run_crawlers/mercado_livre_tenis_corrida_masculino.sh{% endraw %}"
        ) ## Arrumar esse path gigante
        
        run_magalu_crawler = BashOperator(
            task_id="run_magalu_crawler",
            bash_command="{% raw %}cd /usr/local/airflow/datawarehouse/sources/magalu_source/ && sh run_crawlers/magalu_tenis_corrida_masculino.sh{% endraw %}"
        ) ## Arrumar esse path gigante
    
    insert_data_database = PythonOperator(
        task_id="insert_data_db",
        python_callable=insert_data_to_postgres,
        op_kwargs={"schema": "data"},
        provide_context=True
    )
    
    remove_file = PythonOperator(
        task_id="remove_data_from_data_dir",
        python_callable=remove_data_from_dir,
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
            emit_datasets=True
            ),
        execution_config=venv_execution_config,
        default_args={"retries": 3},
    )
    
    data_handling >> run_crawlers >> insert_data_database >> [dbt_tasks, remove_file]