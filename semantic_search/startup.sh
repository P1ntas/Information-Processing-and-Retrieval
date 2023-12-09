docker exec premier_league bin/solr delete -c semantic_articles
docker exec premier_league bin/solr create_core  -c semantic_articles

curl -X POST -H 'Content-type:application/json' \
--data-binary "@../semantic_schema.json" \
http://localhost:8983/solr/semantic_articles/schema


curl -X POST -H 'Content-type:application/json' \
--data-binary "@../documents/semantic_articles.json" \
http://localhost:8983/solr/semantic_articles/update?commit=true


