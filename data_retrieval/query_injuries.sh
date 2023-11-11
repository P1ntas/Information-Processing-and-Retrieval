curl -X GET http://localhost:8983/solr/articles/query?q=%22Coutinho%20injury%22\&q.op=OR\&defType=edismax\&indent=true\&qf=title%5E2.3%20summary%20text%5E0.4\&qs=20\&fl=*,score\&bf=ms\(date,NOW\)\&bq=%7B!parent%20which%3D%22*:*%20-_nest_path_:*%22%7D\(%2B_nest_path_:%5C%2Fnamed_players%20%2Bname:%22Philippe%20Coutinho%22\)\&useParams= >> coutinho_injuries.json

<<comment
curl -X GET http://localhost:8983/solr/articles/query -d  '
{   
    "query": "text:\"Coutinho injury\"~10"
}'
comment




