import psycopg2 as db

conn_string = "dbname='dataengineering' host='172.17.0.3' user='postgres' password='postgres'"
conn = db.connect(conn_string)
cur = conn.cursor()
query2 = "select * from users"

#fetch all records
cur.execute(query2)
print(type(cur.fetchall()))

#iterate over records and print result
cur.execute(query2)
for record in cur:
    print(record)
