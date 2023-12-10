import json

with open('../data_collection/team_nicknames.json', 'r') as json_file:
    data = json.load(json_file)

with open('../solr/synonyms.txt', 'w') as txt_file:

    for team in data['teams']:
        name = team['name']
        csv_name = team['csv_name']
        short_name = team['short_name']
        if len(team['nicknames']) == 0:
            txt_file.write(f"{name},{csv_name},{short_name}\n")
        else:
            nicknames = ','.join(team['nicknames'])
            txt_file.write(f"{name},{csv_name},{nicknames},{short_name}\n")

print("Data has been written to synonyms.txt.")
