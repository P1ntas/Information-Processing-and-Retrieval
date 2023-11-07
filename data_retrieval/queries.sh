curl -X GET http://localhost:8983/solr/games/query -d  '
{
  "query": "_nest_path_:\\/home_team AND {!child of=\"*:* -_nest_path_:*\"}season:2016-17",
  "facet": {
    "teams": {
      "type": "terms",
      "field" : "name",
      "facet" : {
        "goals":{
            "type": "query",
            "facet":{
                "nr_goals": "sum(home_goals)"
            },
            "domain" : {
                "blockParent": "*:* -_nest_path_:*"
            }
        }
      }
    }
  }
}'


curl -X GET http://localhost:8983/solr/games/query -d  '
{
  "query": "_nest_path_:\\/away_team AND {!child of=\"*:* -_nest_path_:*\"}season:2016-17",
  "facet": {
    "teams": {
      "type": "terms",
      "field" : "name",
      "facet" : {
        "goals":{
            "type": "query",
            "facet":{
                "nr_goals": "sum(away_goals)"
            },
            "domain" : {
                "blockParent": "*:* -_nest_path_:*"
            }
        }
      }
    }
  }
}'