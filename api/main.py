from flask import Flask, jsonify, request
from urllib.parse import quote
import requests

def perform_search(query):
    articles_core = "http://localhost:8983/solr/articles/query"
    terms_used = f'"{query}"^10'
    for term in query.split():
        terms_used += " " + term + "^0.2"

    query_independent_part = "q.op=OR&defType=edismax&indent=true&qf=title%5E2.3%20summary%20text%5E0.4&qs=20&fl=*,score&bf=ms(date,NOW)&rows=999&useParams="
    
    solr_query = f"{articles_core}?q={quote(terms_used)}&{query_independent_part}"
    results = requests.get(solr_query).json()['response']['docs']
    return results

app = Flask(__name__)

@app.route('/api/article/<id>')
def get_article(id):
    solr_query = f"http://localhost:8983/solr/articles/query?q=id:{id}&q.op=OR&indent=true&fl=*,%5Bchild%5D&useParams="
    results = requests.get(solr_query).json()['response']['docs']
    return results


@app.route('/api/search')
def search():
    # Retrieve the 'query' parameter from the URL
    query_param = request.args.get('query', default='', type=str)
    
    # Perform some search logic with the query parameter
    results = perform_search(query_param)
    
    # Return the results as JSON
    return jsonify({'results': results})


if __name__ == '__main__':
    app.run(debug=True)


