docker exec evaluation bin/solr delete -c semantic_articles
docker exec evaluation bin/solr create_core  -c semantic_articles

curl -X POST -H 'Content-type:application/json' \
--data-binary "@~/data/semantic_schema.json" \
http://localhost:8983/solr/semantic_articles/schema


curl -X POST -H 'Content-type:application/json' \
--data-binary "@/data/semantic_articles.json" \
http://localhost:8983/solr/semantic_articles/update?commit=true


