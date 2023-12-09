docker exec premier_league bin/solr delete -c most_value_team_transfers
docker exec premier_league bin/solr create_core  -c most_value_team_transfers

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@../../schema.json" \
    http://localhost:8983/solr/most_value_team_transfers/schema

curl -X POST -H 'Content-type:application/json' \
--data-binary "@../../documents/most_valued_team_transfers_period.json" \
    http://localhost:8983/solr/most_value_team_transfers/update?commit=true


docker exec premier_league bin/solr delete -c most_value_team_transfers_schemaless
docker exec premier_league bin/solr create_core  -c most_value_team_transfers_schemaless

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@../../basic_schema.json" \
    http://localhost:8983/solr/most_value_team_transfers_schemaless/schema

curl -X POST -H 'Content-type:application/json' \
--data-binary "@../../documents/most_valued_team_transfers_period.json" \
    http://localhost:8983/solr/most_value_team_transfers_schemaless/update?commit=true


docker exec premier_league bin/solr delete -c most_value_team_transfers_semantic
docker exec premier_league bin/solr create_core  -c most_value_team_transfers_semantic

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@../../semantic_schema.json" \
    http://localhost:8983/solr/most_value_team_transfers_semantic/schema

curl -X POST -H 'Content-type:application/json' \
    --data-binary "@../../documents/most_valued_team_transfers_period_semantic.json" \
    http://localhost:8983/solr/most_value_team_transfers_semantic/update?commit=true
