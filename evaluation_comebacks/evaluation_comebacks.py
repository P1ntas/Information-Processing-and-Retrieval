import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import requests
import pandas as pd
import json
schemaless_file = "schemaless.json"
schemaplus_file = "schemaplus.json"
boost_file = "boosted.json"

with open(schemaless_file, 'r') as file:
    schemaless_data = json.load(file)

with open(schemaplus_file, 'r') as file:
    schemaplus_data = json.load(file)

with open(boost_file, 'r') as file:
    boost_data = json.load(file)
QRELS_FILE = "comebacks_qrels.txt"
relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from Solr instance
schemaless = []
for group in schemaless_data.get('grouped', {}).get('abbreviation', {}).get('groups', []):
    for doc in group.get('doclist', {}).get('docs', []):
        schemaless.append(doc.get('parent').get('docs')[0])

schemaplus = []
for group in schemaplus_data.get('grouped', {}).get('abbreviation', {}).get('groups', []):
    for doc in group.get('doclist', {}).get('docs', []):
        schemaplus.append(doc.get('parent').get('docs')[0])
    
boosted = []
for group in boost_data.get('grouped', {}).get('abbreviation', {}).get('groups', []):
    for doc in group.get('doclist', {}).get('docs', []):
        boosted.append(doc.get('parent').get('docs')[0])

results_list = [schemaless,schemaplus,boosted]
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
                print(doc['url'])
                if doc['url'] in relevant:
                    relevant_count += 1
                    precision_at_k = relevant_count / (idx + 1)
                    precision_values.append(precision_at_k)

            print("\n")
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
