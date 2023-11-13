
#curl -X GET http://localhost:8983/solr/articles/query?q=%22Coutinho%20injury%22\&q.op=OR\&defType=edismax\&indent=true\&qf=title%5E2.3%20summary%20text%5E0.4\&qs=20\&fl=*,score\&bf=ms\(date,NOW\)\&bq=%7B!parent%20which%3D%22*:*%20-_nest_path_:*%22%7D\(%2B_nest_path_:%5C%2Fnamed_players%20%2Bname:%22Philippe%20Coutinho%22\)\&useParams=

curl -o boosted.json -X GET 'http://localhost:8983/solr/comebacks_articles/query?group=true%3Dtrue&group.field=abbreviation&group.limit=10&parent.q={!parent%20which="*:*%20-_nest_path_:*"%20v=\{!terms%20f=id%20v=$row.article_id\}}&fl=*,parent:\[subquery\]' -d '
{
    "query": "_nest_path_:\\/named_teams AND (({!child of=\"*:* -_nest_path_:*\"}title:comeback^2) OR ({!child of=\"*:* -_nest_path_:*\"}summary:comeback^1.5) OR ({!child of=\"*:* -_nest_path_:*\"}text:comeback^1) OR ({!child of=\"*:* -_nest_path_:*\"}title:fightback^2) OR ({!child of=\"*:* -_nest_path_:*\"}summary:fightback^1.5) OR ({!child of=\"*:* -_nest_path_:*\"}text:fightback^1))"
}'

<<comment
curl -X GET http://localhost:8983/solr/articles/query -d  '
{
    "query": "text:\"Oxlade-Chamberlain injury\"~10"
}'

curl -X GET http://localhost:8983/solr/games/query?rows=0 -d  '
{
    "query": "*:* -_nest_path_:*",
    "facet": {
        "seasons":{
            "type": "terms",
            "field" : "season",
            "facet": {
                "type": "query",
                "query": "_nest_path_:\\/home_team OR _nest_path_:\\/away_team",
                "teams": {
                    "facet": {
                        "type": "terms",
                        "field" : "name",
                        "sort": "nr_goals desc",
                        "limit":1,  
                        "facet" : {
                            "nr_goals": "sum(goals)"                
                        }
                    }
                }
            }
        }
    }
}'








curl -X GET http://localhost:8983/solr/games/query -d  '
{
    "query": "_nest_path_:\\/home_team AND {!child of=\"*:* -_nest_path_:*\"}season:2016-17",
    "facet": {
        "teams": {
            "type": "terms",
            "field" : "name",
            "facet" : {
                "nr_goals": "sum(home_goals)",
                "domain" : {
                    "blockParent": "*:* -_nest_path_:*"
                }
            }
        }
    },
}'

curl -X GET http://localhost:8983/solr/games/query -d  '
{
  "query": "_nest_path_:\\/away_team AND {!child of=\"*:* -_nest_path_:*\"}season:2016-17",
  "facet": {
    "teams": {
      "type": "terms",
      "field" : "name",
      "sort": "count"
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
comment
