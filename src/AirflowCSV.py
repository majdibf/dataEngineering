import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import pandas as pd


def csvToJson():
    df = pd.read_csv('/home/project/data.csv')
    for i, r in df.iterrows():
        print(r['name'])
    df.to_json('/home/project/fromAirflow.json', orient='records')


default_args = {
    'owner': 'mbenfredj',
    'start_date': dt.datetime(2024, 1, 4),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('MyCSVDAG',
         default_args=default_args,
         schedule=timedelta(minutes=5),  # '0 * * * *',
         ) as dag:
    print_starting = BashOperator(task_id='starting',
                                  bash_command='echo "I am reading the CSV now....."')

    csvJson = PythonOperator(task_id='convertCSVtoJson',
                             python_callable=csvToJson)

print_starting >> csvJson
