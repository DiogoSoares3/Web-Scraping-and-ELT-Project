#### This is a util file to load new data to database when the crawlers return more json

import polars as pl
import os
from sqlalchemy import create_engine, MetaData, Table, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import inspect, text


ROOT_DIR = './sources' ## Dags will execute from /datawarehouse directory, so we put this as root dir for our load schema
DB_URL = 'postgresql://postgres:postgres@postgres:5432/WebScraping'


def create_schema_if_not_exists(conn, schema_name):
    create_schema_query = text(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")
    conn.execute(create_schema_query)
    conn.commit()
    print(f"Schema '{schema_name}' create or retrieved.")


def load_data_to_postgres(file_path, table_name, schema='public'):
    _, file_extension = os.path.splitext(file_path)

    if file_extension == '.json':
        df = pl.read_json(file_path)
    elif file_extension == '.csv':
        df = pl.read_csv(file_path)
    else:
        raise ValueError("Just .json and .csv files are supported.")

    engine = create_engine(DB_URL, echo=False, future=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        with engine.connect() as conn:
            create_schema_if_not_exists(conn, schema)

        columns = [Column(col, String) for col in df.columns]
        metadata = MetaData(schema=schema)

        table = Table(table_name, metadata, *columns, extend_existing=False)

        inspector = inspect(engine)
        if inspector.has_table(table_name, schema=schema):
            raise ProgrammingError(f"A tabela '{schema}.{table_name}' já existe no banco de dados.")
            ### Aqui talvez seja legal adicionar os novos dados na tabela, ao inves de dar erro quando eu tento adicionar novos dados retornados pelo crawler

        metadata.create_all(engine)

        rows_to_insert = df.to_dicts()
        session.execute(table.insert().values(rows_to_insert))

        session.commit()

    except ProgrammingError as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()


def process_files_in_directory(schema='public'):
    for source_dir in os.listdir(ROOT_DIR):
        if source_dir.endswith('_source'):
            data_dir = os.path.join(ROOT_DIR, source_dir, 'data')

            if not os.path.exists(data_dir):
                continue
            
            # Process all JSON and CSV files on the 'data' directory
            for file_name in os.listdir(data_dir):
                file_path = os.path.join(data_dir, file_name)
                if file_name.endswith('.json') or file_name.endswith('.csv'):
                    table_name = file_name.rsplit('.', 1)[0]  # Table's name based on the file name
                    try:
                        load_data_to_postgres(file_path, table_name, schema)
                        print(f"Data from {file_name} were inserted in the table {table_name}.")
                        os.remove(file_path)
                    except ProgrammingError as e:
                        print(f"Erro: {e}")
                    except Exception as e:
                        print(f"Falha ao processar {file_name}: {e}")


if __name__ == '__main__':
    process_files_in_directory(schema='data')
