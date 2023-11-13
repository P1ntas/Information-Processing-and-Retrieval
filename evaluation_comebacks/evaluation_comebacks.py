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

[[{'id': '10288', 'title': "Ward-Prowse seals Saints' comeback win", 'summary': "Midfielder's free-kick and Danny Ings's sixth goal in eight matches earn 2-1 victory over Watford", 'text': "\n James Ward-Prowse's late free-kick earned  Southampton  a thrilling 2-1 comeback victory against  Watford . \n Ismaila Sarr gave Watford the lead after 24 minutes,\xa0latching on to a long pass down the right before firing high past Alex McCarthy. \n Southampton substitute Shane Long saw his close-range effort tipped on to the crossbar by Ben Foster before Danny Ings equalised with 12 minutes remaining. \n Moussa Djenepo got to the byline with great skill and crossed low for Ings to scramble in\xa0at the near post for his sixth goal in his last eight matches. \n Ward-Prowse completed the comeback on 83 minutes, with Foster unable to prevent his curled free-kick from finding the top-left corner. \n Watford substitute Andre Gray lashed wide in stoppage time but 18th-placed Southampton held on for their first home win of the season to move four points\xa0clear of the Hornets in 20th. \n Next fixtures \n Southampton: 4 Dec v Norwich (H) Watford: 4 Dec v Leicester (A) \n \n \n FT \n \n \n \n \n \n \n \n \n \n Southampton \n SOU \n \n \n \n \n 2 - 1 \n \n \n \n \n \n \n \n \n Watford \n WAT \n \n \n \n \n HT:  \n Half Time:  \n      0-1\n     \n \n \n \n Danny Ings  78'\n               \n \n \n \n \n James Ward-Prowse  83'\n               \n \n \n \n \n \n \n Ismaïla Sarr  24'\n               \n \n \n \n \n \n \n Assists \n \n \n \n Moussa Djenepo  78'\n           \n \n \n \n \n \n \n View Match \n \n \n \n \n", 'date': '2019-11-30T00:00:00Z', 'url': 'https://www.premierleague.com/news/1506930', '_version_': 1782389877813280768}], [{'id': '10469', 'title': 'Brewster inspires comeback win for Liverpool', 'summary': "Striker involved in both goals for Group F leaders against Sunderland as we look at what happened in the weekend's five PL Cup matches", 'text': "\n Rhian Brewster inspired  Liverpool  to a comeback 2-1 victory at  Sunderland  in the  Premier League Cup .\xa0 \n Benji Kimpioka had given the hosts a second-half lead but Brewster forced an own goal from Michael Collins before the 19-year-old won and converted a late penalty.\xa0 \n It keeps the Reds top of Group F with two wins from two matches. Sunderland are third, level with second-placed  Huddersfield Town  and one point above bottom team\xa0 Wigan Athletic .\xa0 \n See:  Sunderland report  |  Liverpool report \n Group B\xa0 \n Watford  came from behind three times to win a 4-3 at  Fulham . \n Fulham went ahead at Motspur Park through Fabio Carvalho, Jayden Harris and Tayo Edun. \n But\xa0Joseph Hungbo, Kaylen Hinds and Sonny Blu Lo-Everton pegged them back before Hungbo scored a second with 18 minutes remaining.\xa0 \n See:  Fulham report  |  Watford report \n In the other match in the group,  Everton  were denied a first win of their PL Cup defence by Plymouth Argyle goalkeeper Mike Cooper in a 1-1 draw.\xa0 \n Cooper was beaten by\xa0Harry Charsley but, after Billy Clarke equalised, he\xa0starred with saves from Oumar Niasse, Kyle John, Ellis Simms and Ryan Astley.\xa0 \n Watford top the group on four points, followed by Fulham, Plymouth and Everton. \n See:  Everton report  |  Plymouth report \n Group E \n Southampton  moved above  AFC Bournemouth  on goal difference at the top with a 3-1 home victory over  Nottingham Forest .\xa0 \n It was 1-1 at the break after goals from Southampton's\xa0Kornelius Hansen and Forest's\xa0Alex Mighten. \n Saints moved to four points from two matches thanks to second-half strikes from\xa0Jake Vokins and Christoph Klarer. \n Forest are bottom, two points behind  Stoke City . \n See:  Southampton report  |  Forest report \n Group H\xa0 \n Benny Ashley-Seal scored twice as leaders\xa0 Wolverhampton Wanderers  beat  Birmingham City  2-1 to go five points clear. \n Bottom club  Derby County  host second-placed  Leeds United  on Wednesday in their match in hand over Wolves.\xa0 \n \n \n \n \n \n SOU \n \n \n \n \n 3 - 1 \n \n NFO \n \n \n \n \n \n \n \n \n \n \n WOL \n \n \n \n \n 2 - 1 \n \n BIR \n \n \n \n \n \n \n \n \n \n \n FUL \n \n \n \n \n 3 - 4 \n \n WAT \n \n \n \n \n \n \n \n \n \n \n SUN \n \n \n \n \n 1 - 2 \n \n LIV \n \n \n \n \n \n \n \n \n \n \n EVE \n \n \n \n \n 1 - 1 \n \n PLY \n \n \n \n \n \n \n \n \n \n \n \n close \n \n \n TV Info \n \n Broadcasters \n \n \n \n \n \n \n", 'date': '2019-11-11T00:00:00Z', 'url': 'https://www.premierleague.com/news/1493489', '_version_': 1782389877907652610}], [{'id': '10356', 'title': 'Man City on the rise after comeback win', 'summary': 'Champions beat Chelsea to go third thanks to goals from Kevin De Bruyne and Riyad Mahrez', 'text': "\n Manchester City rallied from a goal down to beat  Chelsea  2-1 and move above their opponents into third in the Premier League. \n The Londoners' six-match winning run came to an end as the champions bounced back after conceding N'Golo Kante's opening goal. \n Kante struck on 21 minutes when he kept his composure to finish Mateo Kovacic's fine through-ball past the advancing Ederson. \n City equalised eight minutes later when Kevin De Bruyne's shot went in via a deflection off Kurt Zouma. \n Pep Guardiola's side went in front on 37 minutes with a fine individual goal from Riyad Mahrez, who cut in from the right and curled a shot into the bottom corner. \n The closest Chelsea came to a response was when Kante's shot was deflected wide by Fernandinho. \n City have 28 points from 13 matches, two more than the fourth-placed Chelsea, but nine behind leaders Liverpool. \n See:\xa0 Man City report \xa0|\xa0 Chelsea report \n Next fixtures \n Man City: 30 Nov v Newcastle (A) Chelsea: 30 Nov v West Ham (H) \n \n \n FT \n \n \n \n \n \n \n \n \n \n Manchester City \n MCI \n \n \n \n \n 2 - 1 \n \n \n \n \n \n \n \n \n Chelsea \n CHE \n \n \n \n \n HT:  \n Half Time:  \n      2-1\n     \n \n \n \n Kevin De Bruyne  29'\n               \n \n \n \n \n Riyad Mahrez  37'\n               \n \n \n \n \n \n \n N'Golo Kanté  21'\n               \n \n \n \n \n \n \n Assists \n \n \n \n Rodri  37'\n           \n \n \n \n Mateo Kovacic  21'\n           \n \n \n \n \n View Match \n \n \n \n \n", 'date': '2019-11-23T00:00:00Z', 'url': 'https://www.premierleague.com/news/1498889', '_version_': 1782389877866758144}], [{'id': '10551', 'title': 'Robertson and Mane earn comeback win at Villa', 'summary': 'Liverpool score twice in last four minutes to claim 2-1 victory at Villa Park and stay six points clear', 'text': "\n Late goals by Andrew Robertson and Sadio Mane gave Liverpool a dramatic 2-1 comeback victory over Aston Villa to maintain their unbeaten start to the season. \n Anwar El Ghazi forced Alisson into an early save before Trezeguet opened the scoring after 21 minutes. \n John McGinn’s free-kick was finished by Trezeguet, who became the first Egyptian to score for Villa in the Premier League. \n Mane was denied superbly by Villa goalkeeper Tom Heaton, while Mohamed Salah headed over as Liverpool pressed for an equaliser. \n Robertson made it 1-1 with just three minutes remaining, heading in Mane's floated cross at the back post. \n Mane completed the comeback when he glanced in Trent Alexander-Arnold's corner in stoppage time. \n Liverpool have 31 points, six clear of Manchester City, while\xa0Villa lie 15th with 11 points. \n See:  Villa report  |  Liverpool report \n Next fixtures \n Aston Villa:\xa010 Nov v Wolves (A) Liverpool: 10 Nov v Man City (H) \n \n \n FT \n \n \n \n \n \n \n \n \n \n Aston Villa \n AVL \n \n \n \n \n 1 - 2 \n \n \n \n \n \n \n \n \n Liverpool \n LIV \n \n \n \n \n HT:  \n Half Time:  \n      1-0\n     \n \n \n \n Trézéguet  21'\n               \n \n \n \n \n \n \n Andy Robertson  87'\n               \n \n \n \n \n Sadio Mané  90 +4'\n               \n \n \n \n \n \n \n Assists \n \n \n \n John McGinn  21'\n           \n \n \n \n Sadio Mané  87'\n           \n \n Trent Alexander-Arnold  90 +4'\n           \n \n \n \n \n View Match \n \n \n \n \n", 'date': '2019-11-02T00:00:00Z', 'url': 'https://www.premierleague.com/news/1479228', '_version_': 1782389877933867009}]]

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
