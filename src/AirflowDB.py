import datetime as dt
from datetime import timedelta

import pandas as pd
import psycopg2 as db
from airflow import DAG
from airflow.operators.python import PythonOperator
from elasticsearch import Elasticsearch

default_args = {
    'owner': 'mbenfredj',
    'start_date': dt.datetime(2024, 1, 4),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}


def queryPostgresql():
    conn_string = "dbname='dataengineering' host='172.17.0.3' user='postgres' password='postgres'"
    conn = db.connect(conn_string)
    df = pd.read_sql("select name,city from users", conn)
    df.to_csv('/home/project/postgresqldata.csv')
    print("-------Data Saved------")


def insertElasticsearch():
    es = Elasticsearch({'http://172.17.0.3:9200'})
    df = pd.read_csv('postgresqldata.csv')

    for i, r in df.iterrows():
        doc = r.to_json()
        res = es.index(index="frompostgresql",
                       doc_type="doc", body=doc)
        print(res)


with DAG('MyDBdag',
         default_args=default_args,
         schedule=timedelta(minutes=5),  # '0 * * * *',
         ) as dag:
    getData = PythonOperator(task_id="QueryPostgreSQL",
                             python_callable=queryPostgresql)

    insertData = PythonOperator(task_id="InsertDataElasticsearch",
                                python_callable=insertElasticsearch)

getData >> insertData
