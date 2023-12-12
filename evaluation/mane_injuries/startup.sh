#!/bin/bash

#!/bin/sh

mkdir /var/solr/data

precreate-core mane_articles

precreate-core mane_articles_schemaless

precreate-core mane_articles_synonyms

precreate-core semantic_articles

# Start Solr in background mode so we can use the API to upload the schema
solr start

sleep 10

cp /data/synonyms.txt /var/solr/data/mane_articles_synonyms/conf

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/synonym_schema.json \
    http://localhost:8983/solr/mane_articles_synonyms/schema

bin/post -c mane_articles_synonyms /data/articles_mane_injury_period.json

curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/basic_schema.json \
    http://localhost:8983/solr/mane_articles_schemaless/schema

bin/post -c mane_articles_schemaless /data/articles_mane_injury_period.json

curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/schema.json \
    http://localhost:8983/solr/mane_articles/schema

bin/post -c mane_articles /data/articles_mane_injury_period.json

curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/semantic_schema.json \
    http://localhost:8983/solr/semantic_articles/schema

bin/post -c semantic_articles /data/semantic_articles.json

# Restart in foreground mode so we can access the interface
solr restart -f