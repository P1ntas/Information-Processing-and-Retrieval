import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import requests
import pandas as pd
from urllib.parse import quote
from sentence_transformers import SentenceTransformer

def query_articles(query,team_abbreviation,player_name,start,rows):
    articles_core = "http://localhost:8983/solr/most_value_team_transfers_synonyms/select"
    terms_used = ""
    if query:
        main_query = f'"{query}"^10'
        for term in query.split():
            terms_used += " " + term + "^0.2"
        main_query = f"q={quote(main_query + terms_used)}"
    else:
        main_query = 'q=&q.alt=*:*'
        
    query_independent_part = "&q.op=OR&defType=edismax&indent=true&qf=title%5E2.3%20summary%20text%5E0.4&qs=20&fl=*,score&bf=ms(date,NOW)"
    
    
    pagination = f"&rows={rows}&start={start}&useParams="
    
    filter_query=""

    if team_abbreviation and not player_name:
        team_abbreviation = '"' + team_abbreviation + '"'
        filter_query = '&' + f'fq=%7B!parent%20which%3D%22*:*%20-_nest_path_:*%22%7D%28%2B_nest_path_:%5C%2Fnamed_teams%20%2Babbreviation:{quote(team_abbreviation)}%29'
    if player_name and not team_abbreviation:
        player_name = '"' + player_name + '"'
        filter_query = '&' +f'fq=%7B!parent%20which%3D%22*:*%20-_nest_path_:*%22%7D%28%2B_nest_path_:%5C%2Fnamed_players%20%2Bname:{quote(player_name)}%29'

    
    solr_query = f"{articles_core}?{main_query}{query_independent_part}{filter_query}{pagination}"
    return solr_query

def text_to_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text, convert_to_tensor=False).tolist()
    
    # Convert the embedding to the expected format
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    return embedding_str

def solr_knn_query(endpoint, collection, embedding):
    url = f"{endpoint}/{collection}/select"

    data = {
        "q": f"{{!knn f=vector topK=10}}{embedding}",
        "fl": "url",
        "rows": 10,
        "wt": "json"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()

QRELS_FILE = "most_valued_team_transfers_qrels.txt"
QUERY_SCHEMALESS_URL = "http://localhost:8983/solr/most_value_team_transfers_schemaless/query?q=text:%22MCI%20transfer%22%0Atext:%22MCI%20signing%22%0Atext:%22Manchester%20City%20transfer%22%0Atext:%22Manchester%20City%20signing%22%0Atext:MCI%0Atext:%22Manchester%20City%22%0Atext:transfer%0Atext:signing%0Asummary:%22MCI%20transfer%22%0Asummary:%22MCI%20signing%22%0Asummary:%22Manchester%20City%20transfer%22%0Asummary:%22Manchester%20City%20signing%22%0Asummary:MCI%0Asummary:%22Manchester%20City%22%0Asummary:transfer%0Asummary:signing%0Atitle:%22MCI%20transfer%22%0Atitle:%22MCI%20signing%22%0Atitle:%22Manchester%20City%20transfer%22%0Atitle:%22Manchester%20City%20signing%22%0Atitle:MCI%0Atitle:%22Manchester%20City%22%0Atitle:transfer%0Atitle:signing&q.op=OR&indent=true&rows=200&useParams="
QUERY_SCHEMA_URL = "http://localhost:8983/solr/most_value_team_transfers/query?q=text:%22MCI%20transfer%22%0Atext:%22MCI%20signing%22%0Atext:%22Manchester%20City%20transfer%22%0Atext:%22Manchester%20City%20signing%22%0Atext:MCI%0Atext:%22Manchester%20City%22%0Atext:transfer%0Atext:signing%0Asummary:%22MCI%20transfer%22%0Asummary:%22MCI%20signing%22%0Asummary:%22Manchester%20City%20transfer%22%0Asummary:%22Manchester%20City%20signing%22%0Asummary:MCI%0Asummary:%22Manchester%20City%22%0Asummary:transfer%0Asummary:signing%0Atitle:%22MCI%20transfer%22%0Atitle:%22MCI%20signing%22%0Atitle:%22Manchester%20City%20transfer%22%0Atitle:%22Manchester%20City%20signing%22%0Atitle:MCI%0Atitle:%22Manchester%20City%22%0Atitle:transfer%0Atitle:signing&q.op=OR&indent=true&rows=200&useParams="
QUERY_BOOST_URL = "http://localhost:8983/solr/most_value_team_transfers/select?defType=edismax&fl=*%2Cscore&fq=date%3A%5B2022-06-10T00%3A00%3A00Z%20TO%202023-01-31T00%3A00%3A00Z%20%5D&indent=true&q.op=OR&q=%22MCI%20transfer%22%5E15%20%22Manchester City%20transfer%22%5E15%20%22Manchester City%20signing%22%5E15%20%22MCI%20signing%22%5E15%20%22MCI%22%5E3%20%22Manchester City%22%5E3%20%22transfer%22%5E0.7%20%22signing%22%5E0.7&qf=title%5E4%20summary%5E3%20text%5E0.7&rows=1000&useParams="
QUERY_SYNONYM_URL = query_articles("Manchester City Transfer","MCI",None,0,200)

query = "Manchester City Transfer"
embedding = text_to_embedding(query)

relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from Solr instance
results_schemaless = requests.get(QUERY_SCHEMALESS_URL).json()['response']['docs']
results_schema = requests.get(QUERY_SCHEMA_URL).json()['response']['docs']
results_boost = requests.get(QUERY_BOOST_URL).json()['response']['docs']
results_semantic = solr_knn_query("http://localhost:8983/solr","semantic_articles",embedding)['response']['docs']
results_synonym = requests.get(QUERY_BOOST_URL).json()['response']['docs']
results_list = [results_schemaless,results_schema,results_boost,results_semantic,results_synonym]
results_list_names = ["schemaless", "schema","boost","semantic","synonym"]
results_linestyle = ['--', '-', ':','--','-.']

def calculate_metrics(results_list):
    fig, ax = plt.subplots()
    for results_idx, results in enumerate(results_list):
                # METRICS TABLE
        # Define custom decorator to automatically calculate metric based on key
        metrics = {}
        metric = lambda f: metrics.setdefault(f.__name__, f)

        @metric
        def ap(results, relevant):
            """Average Precision"""
            precision_values = []
            relevant_count = 0

            for idx, doc in enumerate(results):
                if doc['url'] in relevant:
                    relevant_count += 1
                    precision_at_k = relevant_count / (idx + 1)
                    precision_values.append(precision_at_k)

            if not precision_values:
                return 0.0

            return sum(precision_values) / len(precision_values)

        @metric
        def p10(results, relevant, n=10):
            """Precision at N"""
            return len([doc for doc in results[:n] if doc['url'] in relevant]) / n

        def calculate_metric(key, results, relevant):
            return metrics[key](results, relevant)

        # Define metrics to be calculated
        evaluation_metrics = {
            'ap': 'Average Precision',
            'p10': 'Precision at 10 (P@10)'
        }

        # Calculate all metrics and export results as LaTeX table
        df = pd.DataFrame([['Metric', 'Value']] +
                            [
                                [evaluation_metrics[m], calculate_metric(m, results, relevant)]
                                for m in evaluation_metrics
                            ]
                            )

        with open(f'results_{results_list_names[results_idx]}.tex', 'w') as tf:
            tf.write(df.style.to_latex())
        # Calculate precision and recall values as we move down the ranked list
        precision_values = [
            len([
                doc
                for doc in results[:idx]
                if doc['url'] in relevant
            ]) / idx
            for idx, _ in enumerate(results, start=1)
        ]

        recall_values = [
            len([
                doc for doc in results[:idx]
                if doc['url'] in relevant
            ]) / len(relevant)
            for idx, _ in enumerate(results, start=1)
        ]

        precision_recall_match = {k: v for k, v in zip(recall_values, precision_values)}
        print(results_list_names[results_idx])
        print(precision_values)
        print(recall_values)

        """
        # Extend recall_values to include traditional steps for a better curve (0.1, 0.2 ...)
        recall_values.extend([step for step in np.arange(0.1, 1.1, 0.1) if step not in recall_values])
        recall_values = sorted(set(recall_values))

        # Extend matching dict to include these new intermediate steps
        for idx, step in enumerate(recall_values):
            if step not in precision_recall_match:
                if recall_values[idx - 1] in precision_recall_match:
                    precision_recall_match[step] = precision_recall_match[recall_values[idx - 1]]
                else:
                    precision_recall_match[step] = precision_recall_match[recall_values[idx + 1]]
        """
        disp = PrecisionRecallDisplay([precision_recall_match.get(r) for r in recall_values], recall_values)
        linestyle=results_linestyle[results_idx]
        disp.plot(name=results_list_names[results_idx],ax=ax)

    plt.xlim(0, 1.05)
    plt.ylim(0, 1.05)
    plt.title('Precision-Recall Curve')
    plt.savefig('precision_recall.pdf')


calculate_metrics(results_list)
