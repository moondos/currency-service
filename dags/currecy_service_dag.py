from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG(
    'currency_service_dag',
    default_args=default_args,
    description='Get currency rates and store in DB',
    schedule_interval='0 0 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

currency_service_task = BashOperator(
    task_id='get_currency_rates',
    bash_command=f'python {os.environ["AIRFLOW_HOME"]}/currency_service.py --currencies KZT UZS AZN MYR --ds 2024-05-30',
    dag=dag,
)