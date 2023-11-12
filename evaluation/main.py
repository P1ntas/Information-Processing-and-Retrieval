import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import requests
import pandas as pd

QRELS_FILE = "mane_injuries_qrels.txt"
QUERY_SCHEMALESS_URL = "http://localhost:8983/solr/mane_articles_schemaless/query?q=text:%22Man%C3%A9%20injury%22%20OR%20summary:%22Man%C3%A9%20injury%22%20OR%20title:%20%22Man%C3%A9%20injury%22%20OR%20text:Man%C3%A9%20OR%20summary:Man%C3%A9%20OR%20title:%20Man%C3%A9%20OR%20text:injury%20OR%20summary:injury%20OR%20title:%20injury&q.op=OR&indent=true&rows=999&useParams="
QUERY_SCHEMA_URL = "http://localhost:8983/solr/mane_articles/query?q=text:%22Man%C3%A9%20injury%22%20OR%20summary:%22Man%C3%A9%20injury%22%20OR%20title:%20%22Man%C3%A9%20injury%22%20OR%20text:Man%C3%A9%20OR%20summary:Man%C3%A9%20OR%20title:%20Man%C3%A9%20OR%20text:injury%20OR%20summary:injury%20OR%20title:%20injury&q.op=OR&indent=true&rows=999&useParams="
QUERY_BOOST_URL = "http://localhost:8983/solr/mane_articles/query?q=%22Man%C3%A9%20injury%22%5E10%20Man%C3%A9%5E0.2%20injury%5E0.2&q.op=OR&defType=edismax&indent=true&qf=title%5E2.3%20summary%20text%5E0.4&qs=20&fl=*,score&bf=ms(date,NOW)&bq=%7B!parent%20which%3D%22*:*%20-_nest_path_:*%22%7D(%2B_nest_path_:%5C%2Fnamed_players%20%2Bname:%22Sadio%20Man%C3%A9%22)&rows=999&useParams="
# Read qrels to extract relevant documents
relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from Solr instance
results_schemaless = requests.get(QUERY_SCHEMALESS_URL).json()['response']['docs']
results_schema = requests.get(QUERY_SCHEMA_URL).json()['response']['docs']
results_boost = requests.get(QUERY_BOOST_URL).json()['response']['docs']
results_list = [results_schemaless,results_schema,results_boost]
results_list_names = ["schemaless", "schema","boost"]
results_linestyle = ['--', '-', ':']

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
