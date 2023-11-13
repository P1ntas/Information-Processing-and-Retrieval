docker exec premier_league bin/solr delete -c comebacks_articles
docker exec premier_league bin/solr create_core -c comebacks_articles

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@../schema.json" \
    http://localhost:8983/solr/comebacks_articles/schema

curl -X POST -H 'Content-type:application/json' \
--data-binary "@../documents/articles_comeback_period.json" \
    http://localhost:8983/solr/comebacks_articles/update?commit=true

docker exec premier_league bin/solr delete -c comebacks_articles_schemaless
docker exec premier_league bin/solr create_core -c comebacks_articles_schemaless

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@../basic_schema.json" \
    http://localhost:8983/solr/comebacks_articles_schemaless/schema

curl -X POST -H 'Content-type:application/json' \
--data-binary "@../documents/articles_comeback_period.json" \
    http://localhost:8983/solr/comebacks_articles_schemaless/update?commit=true