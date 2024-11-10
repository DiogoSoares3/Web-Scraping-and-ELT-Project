"Contains profile mappings used in the project"

from cosmos import ProfileConfig
# from cosmos.profiles import PostgresUserPasswordProfileMapping
from include.constants import dbt_path, venv_execution_config


datawarehouse = ProfileConfig(
    profile_name="datawarehouse",
    target_name="dev",
    profiles_yml_filepath=dbt_path / "profiles.yml"
    # profile_mapping=PostgresUserPasswordProfileMapping(
    #     conn_id="airflow_metadata_db",
    #     profile_args={"schema": "dbt"},
    # ),
)
