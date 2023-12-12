#!/bin/bash

#!/bin/sh

mkdir /var/solr/data

precreate-core most_value_team_transfers_synonyms

precreate-core most_value_team_transfers_schemaless

precreate-core most_value_team_transfers

precreate-core semantic_articles

# Start Solr in background mode so we can use the API to upload the schema
solr start

sleep 10

cp /data/synonyms.txt /var/solr/data/most_value_team_transfers_synonyms/conf

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/synonym_schema.json \
    http://localhost:8983/solr/most_value_team_transfers_synonyms/schema

bin/post -c most_value_team_transfers_synonyms /data/most_valued_team_transfers_period.json

curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/basic_schema.json \
    http://localhost:8983/solr/most_value_team_transfers_schemaless/schema

bin/post -c most_value_team_transfers_schemaless /data/most_valued_team_transfers_period.json

curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/schema.json \
    http://localhost:8983/solr/most_value_team_transfers/schema

bin/post -c most_value_team_transfers /data/most_valued_team_transfers_period.json

curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/semantic_schema.json \
    http://localhost:8983/solr/semantic_articles/schema

bin/post -c semantic_articles /data/semantic_articles.json

# Restart in foreground mode so we can access the interface
solr restart -f