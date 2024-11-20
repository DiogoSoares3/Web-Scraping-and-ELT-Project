import os
import uuid

import polars as pl
from sqlalchemy import create_engine, MetaData, Table, Column, String, inspect, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.dialects.postgresql import UUID
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = './datawarehouse/sources' ## Dags will execute from project's root directory, so we put this as root dir for our load schema.
DB_URL = os.getenv("DB_URL")


def _create_schema_if_not_exists(conn, schema_name):
    create_schema_query = text(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")
    conn.execute(create_schema_query)
    conn.commit()
    print(f"Schema '{schema_name}' create or retrieved.")


def _verify_json_quality(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    if content.strip().endswith(','):
        print("Faltando o colchete de fechamento. Corrigindo...")
        content = content.rstrip()[:-1] + ']'

        with open(file_path, 'w') as f:
            f.write(content)
            
        print("Arquivo corrigido e salvo.")

    else:
        print("O arquivo já está completo.")


def _insert_data(file_path, table_name, schema='data'):
    _verify_json_quality(file_path)
    _, file_extension = os.path.splitext(file_path)

    if file_extension == '.json':
        df = pl.read_json(file_path)
    elif file_extension == '.csv':
        df = pl.read_csv(file_path)
    else:
        raise ValueError("Just .json and .csv files are supported.")
    
    rows_to_insert = df.to_dicts()

    for row in rows_to_insert:
        row['id'] = str(uuid.uuid4())

    df = df.with_columns(pl.Series("id", [row['id'] for row in rows_to_insert]))

    engine = create_engine(DB_URL, echo=False, future=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        with engine.connect() as conn:
            _create_schema_if_not_exists(conn, schema)

        columns = [Column('id', UUID(as_uuid=True), primary_key=True)] + [
            Column(col, String) for col in df.columns if col != 'id'
        ]
        metadata = MetaData(schema=schema)

        table = Table(table_name, metadata, *columns, extend_existing=False)

        # Check if table exists, and create if it doesn't
        inspector = inspect(engine)
        if not inspector.has_table(table_name, schema=schema):
            metadata.create_all(engine)

        # Insert rows into the table
        session.execute(table.insert().values(rows_to_insert))
        session.commit()

    except ProgrammingError as e:
        session.rollback()
        raise e
    finally:
        session.close()


def verify_data_already_exists(source_dir=None):
    if source_dir:
        data_dir = os.path.join(source_dir, 'data')
        
        if not os.path.exists(data_dir):
            print('No data left, already up to date.')


def remove_data_from_dir(data_dir=None):
    if data_dir:
        if os.path.exists(data_dir):
            for file_name in os.listdir(data_dir):
                file_path = os.path.join(data_dir, file_name)
                os.remove(file_path)
    else:
        for source_dir in os.listdir(ROOT_DIR):
            if source_dir.endswith('_source'):
                data_dir = os.path.join(ROOT_DIR, source_dir, 'data')

                if not os.path.exists(data_dir):
                    continue
                
                for file_name in os.listdir(data_dir):
                    file_path = os.path.join(data_dir, file_name)
                    os.remove(file_path)


def insert_data_to_postgres(schema='data', source_dir=None):
    if source_dir:
        data_dir = os.path.join(source_dir, 'data')

        if not os.path.exists(data_dir):
            print('No data left, already up to date.')
            return

        for file_name in os.listdir(data_dir):
            file_path = os.path.join(data_dir, file_name)
            if file_name.endswith('.json') or file_name.endswith('.csv'):
                table_name = 'raw-' + file_name.rsplit('.', 1)[0]  # Table's name based on the file name
                _insert_data(file_path, table_name, schema)

        return data_dir

    else:
        for source_dir in os.listdir(ROOT_DIR):
            if source_dir.endswith('_source'):
                data_dir = os.path.join(ROOT_DIR, source_dir, 'data')

                if not os.path.exists(data_dir):
                    continue

                # Process all JSON and CSV files on the 'data' directory
                for file_name in os.listdir(data_dir):
                    file_path = os.path.join(data_dir, file_name)
                    if file_name.endswith('.json') or file_name.endswith('.csv'):
                        table_name = 'raw-' + file_name.rsplit('.', 1)[0]  # Table's name based on the file name

                        try:
                            _insert_data(file_path, table_name, schema)
                            print(f"Data from {file_name} were inserted in the table {table_name}.")

                        except ProgrammingError as e:
                            print(f"Erro: {e}")
                        except Exception as e:
                            print(f"Falha ao processar {file_name}: {e}")


if __name__ == '__main__':
    insert_data_to_postgres(schema='data')
