import requests
import json

solr_url = "http://localhost:8983/solr/games/query?rows=0"

# Define the query payload
home_goals_query_payload = {
  "query": "_nest_path_:\\/home_team AND {!child of=\"*:* -_nest_path_:*\"}season:2022-23",
  "facet": {
    "teams": {
      "type": "terms",
      "field" : "abbreviation",
      "limit": 100,
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
}

away_goals_query_payload = {
  "query": "_nest_path_:\\/away_team AND {!child of=\"*:* -_nest_path_:*\"}season:2022-23",
  "facet": {
    "teams": {
      "type": "terms",
      "field" : "abbreviation",
      "limit": 100,
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
}

nr_goals_per_team = dict()
response = requests.get(solr_url, json=home_goals_query_payload)

if response.status_code == 200:
    result = response.json()
    with open("goals_per_team.json", "w") as json_file:
        json.dump(result, json_file, indent=2)
    for doc in result["facets"]["teams"]["buckets"]:
        team = doc["val"]
        goals = doc["goals"]["nr_goals"]
        nr_goals_per_team[team] = goals
else:
    print(f"Error: {response.status_code} - {response.text}")


response = requests.get(solr_url, json=away_goals_query_payload)

max_goals = 0
max_goals_team = ""
if response.status_code == 200:
    result = response.json()
    for doc in result["facets"]["teams"]["buckets"]:
        team = doc["val"]
        goals = doc["goals"]["nr_goals"]
        nr_goals_per_team[team] += goals
        if nr_goals_per_team[team]>max_goals:
            max_goals_team = team
            max_goals = nr_goals_per_team[team]
else:
    print(f"Error: {response.status_code} - {response.text}")
    
print("Nr goals per team:")
print(nr_goals_per_team)
print(f"Team with the most goals: {max_goals_team}")

team_of_the_week_request = f"http://localhost:8983/solr/articles/select?defType=edismax&fl=*%2Ctermfreq(text%2C%27{max_goals_team}%27)&fq=date%3A%5B2022-08-01T00%3A00%3A00Z%20TO%202023-07-01T00%3A00%3A00Z%20%5D&indent=true&q.op=OR&q=%22team%20of%20the%20week%22&qf=title%5E2.3%20summary%20text%5E0.4&rows=27&sort=date%20asc&useParams="

response = requests.get(team_of_the_week_request)
nr_players = 0 
if response.status_code == 200:
    result = response.json()
    team_of_the_weeks = result["response"]["numFound"]
    for doc in result["response"]["docs"]:
        nr_players+=doc[f"termfreq(text,'{max_goals_team}')"]
    print(f"Nr players in all team of the weeks: {nr_players}")
    print(f"Total team of the weeks:{team_of_the_weeks}")
    print(f"Average number of players in team of the week:{nr_players/team_of_the_weeks}")
    print("Storing query response to most_goals_team_of_the_week.json")

    with open("most_goals_team_of_the_week.json", "w") as json_file:
        json.dump(result, json_file, indent=2)
else:
    print(f"Error: {response.status_code} - {response.text}")
    