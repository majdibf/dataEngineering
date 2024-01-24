# Utilisez une image de base Debian
FROM debian:12

# Mise à jour des paquets et installation des outils de base
RUN apt-get update && \
    apt-get install -y vim wget curl tar && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Installation de Java

# Télécharger et extraire Java
# Définir le répertoire de travail
WORKDIR /usr/local

# Télécharger et extraire le fichier tar.gz Java depuis l'URL
RUN wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz \
    && tar -xzvf openjdk-11.0.2_linux-x64_bin.tar.gz \
    && rm openjdk-11.0.2_linux-x64_bin.tar.gz

# Définir la variable d'environnement JAVA_HOME
ENV JAVA_HOME=/usr/local/jdk-11.0.2

# Mettre à jour la variable d'environnement PATH pour inclure Java
ENV PATH=$JAVA_HOME/bin:$PATH

# Installation de NiFi
# Télécharger et extraire le fichier tar.gz Apache NiFi depuis l'URL
RUN wget https://archive.apache.org/dist/nifi/1.12.1/nifi-1.12.1-bin.tar.gz \
     && tar -xzvf nifi-1.12.1-bin.tar.gz \
     && rm nifi-1.12.1-bin.tar.gz

# # Définir la variable d'environnement NIFI_HOME
ENV NIFI_HOME=/usr/local/nifi-1.12.1

# # Configuration de NiFi
RUN sed -i 's/nifi.web.http.port=8080/nifi.web.http.port=9301/' $NIFI_HOME/conf/nifi.properties
#####################################################################""
# Installation d'Airflow
RUN python3 -m venv /usr/local/venv
ENV PATH="/usr/local/venv/bin:$PATH"
ENV AIRFLOW_HOME=/usr/local/airflow
ENV PATH=$AIRFLOW_HOME/bin:$PATH

# Installer Apache Airflow et les dépendances nécessaires
RUN pip install "apache-airflow[postgres,slack,celery]==2.8.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.1/constraints-3.8.txt"

# Initialiser la base de données et créer un utilisateur administrateur
RUN airflow db init \
    && airflow users create --role Admin --username admin --email admin@example.com --firstname Admin --lastname User --password admin

RUN sed -i 's/load_examples = True/load_examples = False/' /usr/local/airflow/airflow.cfg

# Exposer le port 8080 pour Airflow
EXPOSE 8080

# Installation d'Elasticsearch
# Créer un utilisateur non privilégié
RUN useradd -m -d /home/elasticsearch elasticsearch

# Télécharger et extraire Elasticsearch depuis l'URL
RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.6.0-linux-x86_64.tar.gz \
    && tar -xzvf elasticsearch-7.6.0-linux-x86_64.tar.gz \
    && rm elasticsearch-7.6.0-linux-x86_64.tar.gz

# Définir le répertoire d'installation d'Elasticsearch
ENV ES_HOME=/usr/local/elasticsearch-7.6.0

# Changer le propriétaire du répertoire Elasticsearch
RUN chown -R elasticsearch:elasticsearch $ES_HOME

COPY elasticsearch.yml $ES_HOME/config/elasticsearch.yml

#Utiliser les commandes sed pour décommenter et modifier les valeurs spécifiées dans le fichier
#RUN sed -i 's/#cluster.name: my-application/cluster.name: DataEngineeringWithPython/' $ES_HOME/config/elasticsearch.yml && \
#    sed -i 's/#node.name: node-1/node.name: OnlyNode/' $ES_HOME/config/elasticsearch.yml && \
#    sed -i 's/#http.host: "localhost"/http.host: 0.0.0.0/' $ES_HOME/config/elasticsearch.yml && \
#    sed -i 's/#xpack.ml.enabled: true/xpack.ml.enabled: false/' $ES_HOME/config/elasticsearch.yml

# Exposer le port 9200 pour l'accès à Elasticsearch
EXPOSE 9200

# Installation de Kibana
# Téléchargement et extraction de Kibana depuis l'URL
RUN wget https://artifacts.elastic.co/downloads/kibana/kibana-7.6.2-linux-x86_64.tar.gz && \
    tar xvzf kibana-7.6.2-linux-x86_64.tar.gz -C /usr/local/ && \
    rm kibana-7.6.2-linux-x86_64.tar.gz
ENV KIBANA_HOME=/usr/local/kibana-7.6.2-linux-x86_64

RUN chown -R elasticsearch:elasticsearch $KIBANA_HOME

COPY kibana.yml $KIBANA_HOME/config/kibana.yml

# Configuration de Kibana
#RUN sed -i 's/http.host: 0.0.0.0/http.host: 0.0.0.0/' $KIBANA_HOME/config/kibana.yml

# Exposer le port de Kibana
EXPOSE 5601

# Installation de PostgreSQL
RUN apt-get update && \
    apt-get -y install postgresql

# Configuration de l'utilisateur postgres et création de la base de données
USER postgres

# Définition du mot de passe pour l'utilisateur postgres
RUN /etc/init.d/postgresql start && \
    psql --command "ALTER USER postgres WITH PASSWORD 'postgres';" && \
    createdb dataengineering

# Afficher la version de PostgreSQL
RUN psql --version

# Autoriser les connexions de toutes les adresses IP avec un mot de passe
RUN echo "host    all             all             0.0.0.0/0            md5" >> /etc/postgresql/15/main/pg_hba.conf

# Arrêt du serveur PostgreSQL
RUN /etc/init.d/postgresql stop

# Revenir à l'utilisateur root
USER root

# Exposer les ports de PostgreSQL
EXPOSE 5432

# Exposer les ports nécessaires
EXPOSE 8080 9301 9200 9300 8081

COPY startAll.sh /usr/local/myScripts/startAll.sh
COPY stopAll.sh /usr/local/myScripts/stopAll.sh
COPY restartAll.sh /usr/local/myScripts/restartAll.sh

RUN chmod +x /usr/local/myScripts/*

# Commande pour démarrer tous les services
CMD /usr/local/myScripts/startAll.sh && tail -f /dev/null