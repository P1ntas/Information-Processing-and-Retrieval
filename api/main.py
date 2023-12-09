from fastapi import FastAPI
from fastapi.responses import JSONResponse
from urllib.parse import quote
import asyncio
import httpx
import uvicorn
from PrettyJsonResponse import PrettyJSONResponse
app = FastAPI()

async def async_request(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=None)
        return response.json()

async def query_articles(query):
    articles_core = "http://localhost:8983/solr/articles/query"
    terms_used = f'"{query}"^10'
    for term in query.split():
        terms_used += " " + term + "^0.2"

    query_independent_part = "q.op=OR&defType=edismax&indent=true&qf=title%5E2.3%20summary%20text%5E0.4&qs=20&fl=*,score&bf=ms(date,NOW)&rows=999&useParams="
    
    solr_query = f"{articles_core}?q={quote(terms_used)}&{query_independent_part}"
    results = await async_request(solr_query)
    return results['response']['docs']

async def query_teams(query):
    solr_query = f'http://localhost:8983/solr/teams/query?q=name:%22{quote(query)}%22%20-_nest_path_:*&q.op=OR&indent=true&fl=*,%5Bchild%5D&useParams='
    results = await async_request(solr_query)
    return results['response']['docs']

async def query_players(query):
    solr_query = f'http://localhost:8983/solr/players/query?q=name:%22{quote(query)}%22%20-_nest_path_:*&q.op=OR&indent=true&fl=*,%5Bchild%5D&useParams='
    results = await async_request(solr_query)
    return results['response']['docs']

@app.get('/api/article/{id}',response_class=PrettyJSONResponse)
async def get_article(id: str):
    solr_query = f"http://localhost:8983/solr/articles/query?q=id:{id}&q.op=OR&indent=true&fl=*,%5Bchild%5D&useParams="
    results = await async_request(solr_query)
    return results['response']['docs']

@app.get('/api/search',response_class=PrettyJSONResponse)
async def search(query: str = ''):
    teams_results, players_results, articles_results = await asyncio.gather(
        query_teams(query),
        query_players(query),
        query_articles(query)
    )

    return {
        'teams': teams_results,
        'players': players_results,
        'articles': articles_results
    }

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)
