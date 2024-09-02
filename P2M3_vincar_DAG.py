'''
==================================================================================================
Milestone 3

Nama  : Vincar
Batch : HCK-018

This program is created to automate data loading from postgres, 
preprocessing the column names, and uploading to elasticsearch
==================================================================================================
'''

# Import library
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from sqlalchemy import create_engine
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# Global connection details
database = "airflow_m3"
username = "airflow_m3"
password = "airflow_m3"
host = "postgres"
postgres_url = f"postgresql+psycopg2://{username}:{password}@{host}/{database}"

# Function to create and return a connection
def get_postgres_connection():
    engine = create_engine(postgres_url)
    return engine.connect()


# Function to load csv into postgres
def load_csv_to_postgres():
    # Establish connection
    conn = get_postgres_connection()

    # Read csv
    df = pd.read_csv('/opt/airflow/dags/P2M3_vincar_data_raw.csv')

    # Convert to sql
    df.to_sql('table_m3', conn, index=False, if_exists='replace')

    # Print result  
    print(f"Loaded {len(df)} records into PostgreSQL from CSV.")


# Function to get data from the postgres
def get_data():
    # Establish connection
    conn = get_postgres_connection()

    # Read sql and selecting all
    df = pd.read_sql_query("select * from table_m3", conn) 

    # Convert to csv
    df.to_csv('/opt/airflow/dags/P2M3_vincar_data_new.csv', sep=',', index=False)

    # Print result 
    print(f"Extracted {len(df)} records from PostgreSQL to CSV.")


# Function to preprocess data
def preprocessing():
    # Read csv
    df = pd.read_csv("/opt/airflow/dags/P2M3_vincar_data_new.csv")

    # Add ID column
    df['ID'] = range(1, len(df) + 1)

    # Drop duplicates
    initial_count = len(df)
    df.drop_duplicates(inplace=True)
    duplicate_count = initial_count - len(df)

    # Clean column names (lowercase, remove whitespace, remove special characters)
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace(r'[^a-zA-Z0-9_]', '')

    # Drop rows with missing values
    missing_count = df.isnull().sum().sum()
    df.dropna(inplace=True)

    # Save processed data to csv
    df.to_csv('/opt/airflow/dags/P2M3_vincar_data_clean.csv', index=False)

    # Print result
    print(f"Preprocessed data: removed {duplicate_count} duplicates and {missing_count} rows with missing values. Final record count: {len(df)}.")


def upload_to_elasticsearch():
    # Connect to elasticsearch
    es = Elasticsearch("http://elasticsearch:9200")

    # Read csv
    df = pd.read_csv('/opt/airflow/dags/P2M3_vincar_data_clean.csv')

    # Prepare for bulk to process data faster
    actions = [
        {
            "_index": "table_m3", # Set index to table_m3
            "_id": i+1, # Process all data index+1
            "_source": r.to_dict(), # Convert to dictionary
        }
        for i, r in df.iterrows()
    ]

    # Bulk process
    success, failed = bulk(es, actions, index="table_m3", raise_on_error=False)

    # Print results
    print(f"Successfully uploaded {success} documents")
    print(f"Failed to upload {len(failed)} documents")


# Set owner and start date
default_args = {
    'owner': 'Vincar', 
    'start_date': datetime(2023, 12, 24, 12, 00)
}

# Set DAG name, interval
with DAG(
    "P2M3_Vincar_DAG",
    description='Milestone_3',
    schedule_interval='30 6 * * *', 
    default_args=default_args, 
    catchup=False
) as dag:
    
    # Set Task 1
    load_csv_task = PythonOperator(
        task_id='load_csv_to_postgres',
        python_callable=load_csv_to_postgres)
    
    # Set Task 2
    get_data_pg = PythonOperator(
        task_id='get_data_postgres',
        python_callable=get_data)
    
    # Set Task 3
    edit_data = PythonOperator(
        task_id='edit_data',
        python_callable=preprocessing)

    # Set Task 4
    upload_data = PythonOperator(
        task_id='upload_data_elastic',
        python_callable=upload_to_elasticsearch)

    # Set Task Flow
    load_csv_task >> get_data_pg >> edit_data >> upload_data
