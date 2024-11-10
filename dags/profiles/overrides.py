from datetime import datetime

from cosmos import DbtDag, ProjectConfig, ProfileConfig, RenderConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping

from include.constants import dbt_path, venv_execution_config

dbt_profile_overrides = DbtDag(
    # dbt/cosmos-specific parameters
    project_config=ProjectConfig(dbt_path),
    profile_config=ProfileConfig(
        # these map to dbt/jaffle_shop/profiles.yml
        profile_name="datawarehouse",
        target_name="dev",
        profiles_yml_filepath=dbt_path / "profiles.yml",
        # profile_mapping=PostgresUserPasswordProfileMapping(
        #     conn_id="airflow_metadata_db",
        #     profile_args={
        #                   "database": "postgres",
        #                   "schema": "public"
        #                   },
        # ),
    ),
    render_config=RenderConfig(
        emit_datasets=False
    ),
    execution_config=venv_execution_config,
    # normal dag parameters
    schedule_interval="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    dag_id="dbt_profile_overrides",
    tags=["profiles"],
)
