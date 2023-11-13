import json
from datetime import datetime, timedelta

def filter_documents_by_dates(input_file, output_file, dates):
    # Read the JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    matching_documents = []

    for date_str in dates:
        # Convert the date to a datetime object
        target_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")

        # Identify documents up to 3 days after the target date
        documents_for_date = [
            doc for doc in data
            if target_date <= datetime.strptime(doc.get('date'), "%Y-%m-%dT%H:%M:%SZ") <= target_date + timedelta(days=4)
        ]

        matching_documents.extend(documents_for_date)

    # Write the selected documents to the output file
    with open(output_file, 'w') as f:
        json.dump(matching_documents, f, indent=2)

# Example usage:
input_file_path = '../../documents/articles.json'
output_file_path = '../../documents/articles_mane_injury_period.json'
dates_list = ['2017-04-03T00:00:00Z', '2017-10-09T00:00:00Z', '2020-01-26T00:00:00Z']

filter_documents_by_dates(input_file_path, output_file_path, dates_list)