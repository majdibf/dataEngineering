#!/bin/bash

# Stop Apache NiFi
$NIFI_HOME/bin/nifi.sh stop

# Stop Apache Airflow
pkill -f "airflow webserver"
pkill -f "airflow scheduler"

# Stop Elasticsearch
pkill -f elasticsearch

# Stop Kibana
pkill -f kibana

# Stop PostgreSQL Database
su -s /bin/bash -c "/etc/init.d/postgresql stop" postgres