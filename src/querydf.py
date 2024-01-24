import psycopg2 as db
import pandas as pd
conn_string="dbname='dataengineering' host='172.17.0.3' user='postgres' password='postgres'"
conn=db.connect(conn_string)
df=pd.read_sql("select * from users", conn)
print(df.head())
print(df['city'].value_counts())