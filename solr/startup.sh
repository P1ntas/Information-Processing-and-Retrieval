#!/bin/bash

#!/bin/sh

mkdir /var/solr/data

precreate-core games

precreate-core articles

precreate-core teams

# Start Solr in background mode so we can use the API to upload the schema
solr start

sleep 10

cp /data/synonyms.txt /var/solr/data/games/conf

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/schema.json \
    http://localhost:8983/solr/games/schema

bin/post -c games /data/games.json

cp /data/synonyms.txt /var/solr/data/articles/conf

curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/schema.json \
    http://localhost:8983/solr/articles/schema

bin/post -c articles /data/articles.json

cp /data/synonyms.txt /var/solr/data/teams/conf

curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/schema.json \
    http://localhost:8983/solr/teams/schema

bin/post -c teams /data/teams.json

# Restart in foreground mode so we can access the interface
solr restart -f