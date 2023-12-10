#!/bin/bash

# docker run -p 8983:8983 --name premier_league -v ${PWD}:/data -d solr:9.3

docker exec premier_league bin/solr delete -c games
docker exec premier_league bin/solr create_core  -c games

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@../synonyms.txt" \
    http://localhost:8983/solr/games/update?commit=true&wt=json&file=synonyms.txt&contentType=text/plain;charset=utf-8

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
    --data-binary "@../synonyms.txt" \
    http://localhost:8983/solr/articles/update?commit=true&wt=json&file=synonyms.txt&contentType=text/plain;charset=utf-8

curl -X POST -H 'Content-type:application/json' \
    --data-binary "@../schema.json" \
    http://localhost:8983/solr/articles/schema

curl -X POST -H 'Content-type:application/json' \
--data-binary "@../documents/articles.json" \
    http://localhost:8983/solr/articles/update?commit=true


docker exec premier_league bin/solr delete -c teams
docker exec premier_league bin/solr create_core  -c teams

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@../schema.json" \
    http://localhost:8983/solr/teams/schema

curl -X POST -H 'Content-type:application/json' \
--data-binary "@../documents/teams.json" \
    http://localhost:8983/solr/teams/update?commit=true


docker exec premier_league bin/solr delete -c players
docker exec premier_league bin/solr create_core  -c players

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@../schema.json" \
    http://localhost:8983/solr/players/schema

curl -X POST -H 'Content-type:application/json' \
--data-binary "@../documents/players.json" \
    http://localhost:8983/solr/players/update?commit=true