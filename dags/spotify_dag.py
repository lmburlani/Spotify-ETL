"""Airflow DAG definition for the Spotify ETL pipeline."""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from spotify_etl import run_spotify_etl


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2020, 11, 8),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="spotify_dag",
    default_args=default_args,
    description="Daily Spotify ETL pipeline",
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:
    run_etl = PythonOperator(
        task_id="whole_spotify_etl",
        python_callable=run_spotify_etl,
    )

run_etl
