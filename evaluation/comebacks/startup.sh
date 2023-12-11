#!/bin/bash

#!/bin/sh

mkdir /var/solr/data

precreate-core comebacks_articles

precreate-core comebacks_articles_schemaless

precreate-core comebacks_articles_synonyms

# Start Solr in background mode so we can use the API to upload the schema
solr start

sleep 10

cp /data/synonyms.txt /var/solr/data/comebacks_articles_synonyms/conf

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/synonym_schema.json \
    http://localhost:8983/solr/comebacks_articles_synonyms/schema

bin/post -c comebacks_articles_synonyms /data/articles_comeback_period.json

curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/basic_schema.json \
    http://localhost:8983/solr/comebacks_articles_schemaless/schema

bin/post -c comebacks_articles_schemaless /data/articles_comeback_period.json

curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/schema.json \
    http://localhost:8983/solr/comebacks_articles/schema

bin/post -c comebacks_articles /data/articles_comeback_period.json

# Restart in foreground mode so we can access the interface
solr restart -f