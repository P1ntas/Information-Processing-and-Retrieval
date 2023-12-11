#!/bin/bash

mkdir /var/solr/data

precreate-core games

precreate-core articles

precreate-core teams

precreate-core players

# Start Solr in background mode so we can use the API to upload the schema
solr start

sleep 30

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./schema.json" \
    http://localhost:8983/solr/games/schema

curl -X POST -H 'Content-type:application/json' \
--data-binary "@./documents/games.json" \
    http://localhost:8983/solr/games/update?commit=true




# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./schema.json" \
    http://localhost:8983/solr/articles/schema

curl -X POST -H 'Content-type:application/json' \
--data-binary "@./documents/articles.json" \
    http://localhost:8983/solr/articles/update?commit=true


curl -X POST -H 'Content-type:application/json' -d '{
  "add-requesthandler": {
    "name": "/mlt",
    "class": "solr.MoreLikeThisHandler",
    "defaults": {"mlt.fl": "title"}
  } 
}' http://localhost:8983/solr/articles/config


curl -X POST -H 'Content-type:application/json' -d '{
  "update-searchcomponent": {
    "name": "spellcheck",
    "class": "solr.SpellCheckComponent",
    "spellchecker": {
        "classname": "solr.IndexBasedSpellChecker",
        "spellcheckIndexDir": "./spellchecker",
        "field": "textLittleAnalysis",
        "buildOnCommit": "true"
    }
  } 
}' http://localhost:8983/solr/articles/config

curl -X POST -H 'Content-type:application/json' -d '{
  "update-requesthandler": {
    "name": "/query",
    "class": "solr.SearchHandler",
    "last-components": [
        "spellcheck"
    ]
  } 
}' http://localhost:8983/solr/articles/config


curl -X POST -H 'Content-type:application/json'  -d '{
  "add-searchcomponent": {
    "name": "suggest",
    "class": "solr.SuggestComponent",
    "suggester": {
        "name": "mySuggester",
        "lookupImpl": "BlendedInfixLookupFactory",
        "dictionaryImpl": "DocumentDictionaryFactory",
        "field": "titleLittleAnalysis",
        "suggestAnalyzerFieldType": "textLittleAnalysis",
        "highlight":"false"
    }
  }
}' http://localhost:8983/solr/articles/config


curl -X POST -H 'Content-type:application/json'  -d '{
  "add-requesthandler": {
    "name": "/suggest",
        "class": "solr.SearchHandler",
        "defaults": {
            "suggest": true,
            "suggest.count": 5,
            "suggest.dictionary": "mySuggester"
        },
        "components": [
            "suggest"
        ]
  }
}' http://localhost:8983/solr/articles/config

curl 'http://localhost:8983/solr/articles/suggest?suggest.build=true'



# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./schema.json" \
    http://localhost:8983/solr/teams/schema

curl -X POST -H 'Content-type:application/json' \
--data-binary "@./documents/teams.json" \
    http://localhost:8983/solr/teams/update?commit=true



# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./schema.json" \
    http://localhost:8983/solr/players/schema

curl -X POST -H 'Content-type:application/json' \
--data-binary "@./documents/players.json" \
    http://localhost:8983/solr/players/update?commit=true


solr restart -f