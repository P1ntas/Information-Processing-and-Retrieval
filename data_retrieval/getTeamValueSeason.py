import requests

def parseString(string):
    string = string.replace(',', '.')
    value_list = string.split(" ")
    if value_list[1] == "M":
        value = float(value_list[0]) * 1000000
    elif value_list[1] == "mil":
        value = float(value_list[0]) * 1000000 * 1000
    return value

test_url = "http://localhost:8983/solr/teams/query?q=%7B!parent%20which%3D\"*:*%20-_nest_path_:*\"%7D(%2B_nest_path_:%5C%2Fteam_stats%20%2Bseason_id:22)&q.op=OR&indent=true&rows=20&fl=*,%5Bchild%20childFilter%3Dseason_id:22%5D&useParams="

response = requests.get(test_url)

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

