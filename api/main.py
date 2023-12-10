from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from urllib.parse import quote
import asyncio
import httpx
import uvicorn
from PrettyJsonResponse import PrettyJSONResponse

app = FastAPI()

origins = [
    "*",  # Add the origin of your React app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Use the list of origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"]  # Exposes all headers
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"]  # Exposes all headers
)

async def async_request(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=None)
        return response.json()

async def query_articles(query,start,rows):
    articles_core = "http://localhost:8983/solr/articles/query"
    terms_used = f'"{query}"^10'
    #for term in query.split(): /*generation query/*
    #    terms_used += " " + term + "^0.2"
    query_independent_part = f"q.op=OR&defType=edismax&indent=true&qf=title%5E2.3%20summary%20text%5E0.4&qs=20&fl=*,score&bf=ms(date,NOW)&rows={rows}&start={start}&useParams="
    
    solr_query = f"{articles_core}?q={quote(terms_used)}&{query_independent_part}"
    results = await async_request(solr_query)
    response = results['response']
    docs = response['docs']
    numFound = response['numFound']
    return docs,numFound

async def query_teams(query):
    solr_query = f'http://localhost:8983/solr/teams/query?q=name:%22{quote(query)}%22%20-_nest_path_:*&q.op=OR&indent=true&fl=*,%5Bchild%5D&rows=1&start=0&useParams='
    results = await async_request(solr_query)
    return results['response']['docs']

async def query_players(query):
    solr_query = f'http://localhost:8983/solr/players/query?q=name:%22{quote(query)}%22%20-_nest_path_:*&q.op=OR&indent=true&fl=*,%5Bchild%5D&rows=1&start=0&useParams='
    results = await async_request(solr_query)
    return results['response']['docs']

@app.get('/api/article/{id}',response_class=PrettyJSONResponse)
async def get_article(id: str):
    
    solr_query = f"http://localhost:8983/solr/articles/query?mlt.fl=title,summary,text&mlt.mindf=5&mlt.mintf=3&mlt=true&q=id:{id}&q.op=OR&indent=true&fl=*,%5Bchild%5D&useParams="
    results = await async_request(solr_query)
    articles = results['response']['docs']
    if articles:
        if "moreLikeThis" in results and id in results["moreLikeThis"]:
            return {    
                        "article":articles[0],
                        "moreLikeThis":results["moreLikeThis"][id]["docs"]
                    }
        else:
            return {    
                "article":articles[0] if articles else {},
                "moreLikeThis":{}
            }
    else:
        return {}


@app.get('/api/search',response_class=PrettyJSONResponse)
async def search(query: str = '',start:int=0,rows:int=10):
    teams_results, players_results, (articles_results,numFound) = await asyncio.gather(
        query_teams(query),
        query_players(query),
        query_articles(query,start,rows)
    )
    
    return {
        'team': teams_results[0] if teams_results else {},
        'player': players_results[0] if players_results else {},
        'articles': {
            "numFound": numFound,
            "results":articles_results
        }
    }

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=5000,reload=True)
