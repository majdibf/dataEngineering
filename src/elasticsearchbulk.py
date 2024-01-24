import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from faker import Faker

print(elasticsearch.__version__)

fake = Faker()
es=Elasticsearch({'http://172.17.0.3:9200'})


actions = [
    {
        "_index": "users",
        "_type": "doc",
        "_source": {
            "name": fake.name(),
            "street": fake.street_address(),
            "city": fake.city(),
            "zip": fake.zipcode()}
    }
    for x in range(998)  # or for i,r in df.iterrows()
]

response = helpers.bulk(es, actions)
print(response)
