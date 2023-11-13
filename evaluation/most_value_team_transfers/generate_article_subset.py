import json
from datetime import datetime, timedelta

def filter_documents_by_dates(input_file, output_file, summer):
    # Read the JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    documents = []

    summerBegin = datetime.strptime(summer[0], "%Y-%m-%dT%H:%M:%SZ")
    summerEnd = datetime.strptime(summer[1], "%Y-%m-%dT%H:%M:%SZ")

    documents.extend([doc for doc in data
            if summerBegin <= datetime.strptime(doc.get('date'), "%Y-%m-%dT%H:%M:%SZ") <= summerEnd])
    
    print(len(documents))

    # Write the selected documents to the output file
    with open(output_file, 'w') as f:
        json.dump(documents, f, indent=2)

# Example usage:
input_file_path = '../../documents/articles.json'
output_file_path = '../../documents/most_valued_team_transfers_period.json'
summer = ['2022-06-10T00:00:00Z', '2022-08-01T00:00:00Z']

filter_documents_by_dates(input_file_path, output_file_path, summer)