from datetime import datetime

from cosmos import DbtDag, ProjectConfig, RenderConfig

from include.constants import dbt_path, venv_execution_config
from include.profiles import datawarehouse


dbt_profile_example = DbtDag(
    project_config=ProjectConfig(dbt_path),
    profile_config=datawarehouse,
    render_config=RenderConfig(
        emit_datasets=False
    ),
    execution_config=venv_execution_config,
    schedule_interval="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    dag_id="dbt_profile_example",
    tags=["profiles"],
)
