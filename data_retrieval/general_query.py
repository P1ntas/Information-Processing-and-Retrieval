import sys
import requests
import json

def buildString(input_string):
    stringList = input_string.split()
    finalString = ""
    for string in stringList:
        finalString += "%22" + string + "%22%5E0.5%20"
    return finalString

def buildQuery(input_string):
    query = f"http://localhost:8983/solr/articles/select?defType=edismax&fl=*%2Cscore&indent=true&q.op=OR&q=%22{input_string}%22%5E15%20" + buildString(input_string) + "&bf=ms(date,NOW)&qf=title%5E4%20summary%5E3%20text%5E0.7&rows=100&useParams="
    response = requests.get(query)
    if response.status_code == 200:
        results = response.json()
        with open(f'results_{input_string}.json', 'w') as json_file:
            json.dump(results, json_file, indent=2)
    else:
        print(f"Error: {response.status_code} - {response.text}")
        

input_string = sys.argv[1]
buildQuery(input_string)
