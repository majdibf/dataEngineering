#!/bin/bash
# Start Apache NiFi
echo "Starting Apache NiFi"
$NIFI_HOME/bin/nifi.sh start
sleep 10
# Start Apache Airflow
echo "Starting Apache Airflow webserver"
airflow webserver &
sleep 10
echo "Starting Apache Airflow scheduler"
airflow scheduler &
sleep 10
# Start Elasticsearch
echo "Starting Elasticsearch"
su -s /bin/bash -c "$ES_HOME/bin/elasticsearch -d" elasticsearch
sleep 10

# Start Kibana
echo "Starting Kibana"
su -s /bin/bash -c "$KIBANA_HOME/bin/kibana &" elasticsearch
sleep 10
# Start PostgreSQL Database
echo "Starting PostgreSQL Database"
su -s /bin/bash -c "/etc/init.d/postgresql start" postgres