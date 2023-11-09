#!/bin/bash

# docker run -p 8983:8983 --name premier_league -v ${PWD}:/data -d solr:9.3
docker exec premier_league bin/solr delete -c games
docker exec premier_league bin/solr create_core  -c games

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@../schema.json" \
    http://localhost:8983/solr/games/schema

curl -X POST -H 'Content-type:application/json' \
--data-binary "@../documents/games.json" \
    http://localhost:8983/solr/games/update?commit=true



docker exec premier_league bin/solr delete -c articles
docker exec premier_league bin/solr create_core  -c articles

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@../schema.json" \
    http://localhost:8983/solr/articles/schema

curl -X POST -H 'Content-type:application/json' \
--data-binary "@../documents/articles.json" \
    http://localhost:8983/solr/articles/update?commit=true