import requests
import json

def parseString(string):
    string = string.replace(',', '.')
    value_list = string.split(" ")
    if value_list[1] == "M":
        value = float(value_list[0]) * 1000000
    elif value_list[1] == "mil":
        value = float(value_list[0]) * 1000000 * 1000
    return value

teams_url = "http://localhost:8983/solr/teams/query?q=%7B!parent%20which%3D\"*:*%20-_nest_path_:*\"%7D(%2B_nest_path_:%5C%2Fteam_stats%20%2Bseason_id:22)&q.op=OR&indent=true&rows=20&fl=*,%5Bchild%20childFilter%3Dseason_id:22%5D&useParams="

response = requests.get(teams_url)

max_value = 0

if response.status_code == 200:
    result = response.json()
    for doc in result["response"]["docs"]:
        for stats in doc["team_stats"]:
            if type(stats) is not str:
                value = parseString(stats["team_total_player_value"])
                if value > max_value:
                    max_value_team = doc["name"]
                    max_value_abbreviation = doc["abbreviation"]
                    max_value = value
else:
    print(f"Error: {response.status_code} - {response.text}")

print(f"{max_value_team} ({max_value_abbreviation}) is the team with the highest total value: {max_value} €")

def buildQuery(abbreviation):
    with open("../data_collection/team_nicknames.json", "r") as json_file:
        teams = json.load(json_file)
    for team in teams["teams"]:
        if team["short_name"] == abbreviation:
            team_name = team["csv_name"]
            break
            
    return f"%22{abbreviation}%20transfer%22%5E15%20%22{team_name}%20transfer%22%5E15%20%22{team_name}%20signing%22%5E15%20%22{abbreviation}%20signing%22%5E15%20%22{abbreviation}%22%5E3%20%22{team_name}%22%5E3%20%22transfer%22%5E0.7%20%22signing%22%5E0.7"

transfer_request = f"http://localhost:8983/solr/articles/select?defType=edismax&fl=*%2Cscore&fq=date%3A%5B2022-06-10T00%3A00%3A00Z%20TO%202023-01-31T00%3A00%3A00Z%20%5D&indent=true&q.op=OR&q={buildQuery(max_value_abbreviation)}&qf=title%5E4%20summary%5E3%20text%5E0.7&rows=1000&useParams="

response = requests.get(transfer_request)

if response.status_code == 200:
    result = response.json()
    transfers = result["response"]["numFound"]
    with open("most_valued_team_transfers.json", "w") as json_file:
        json.dump(result, json_file, indent=2)
else:
    print(f"Error: {response.status_code} - {response.text}")

print(f"{max_value_team} ({max_value_abbreviation}) has {transfers} transfers in the news")

