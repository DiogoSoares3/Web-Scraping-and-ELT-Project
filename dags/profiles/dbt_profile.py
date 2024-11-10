from datetime import datetime

from cosmos import DbtDag, ProjectConfig, ProfileConfig, RenderConfig

from include.constants import dbt_path, venv_execution_config
from include.profiles import datawarehouse

# dbt_profile_example = DbtDag(
#     # dbt/cosmos-specific parameters
#     project_config=ProjectConfig(dbt_path),
#     profile_config=ProfileConfig(
#         # these map to dbt/jaffle_shop/profiles.yml
#         profile_name="airflow_db",
#         target_name="dev",
#         profiles_yml_filepath=dbt_path / "profiles.yml",
#     ),
#     render_config=RenderConfig(
#         emit_datasets=False
#     ),
#     execution_config=venv_execution_config,
#     # normal dag parameters
#     schedule_interval="@daily",
#     start_date=datetime(2023, 1, 1),
#     catchup=False,
#     dag_id="dbt_profile_example",
#     tags=["profiles"],
# )


dbt_profile_example = DbtDag(
    # dbt/cosmos-specific parameters
    project_config=ProjectConfig(dbt_path),
    profile_config=datawarehouse,
    render_config=RenderConfig(
        emit_datasets=False
    ),
    execution_config=venv_execution_config,
    # normal dag parameters
    schedule_interval="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    dag_id="dbt_profile_example",
    tags=["profiles"],
)
