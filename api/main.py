from fastapi import FastAPI
from urllib.parse import quote
import asyncio
import httpx
import uvicorn
from PrettyJsonResponse import PrettyJSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def async_request(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=None)
        return response.json()

async def query_articles(query,team_abbreviation,player_name,start,rows):
    articles_core = "http://localhost:8983/solr/articles/query"
    if query:
        main_query = f'"{query}"^10'
        #for term in query.split(): /*generation query/*
        #    terms_used += " " + term + "^0.2"
        main_query = f"q={quote(main_query)}"
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
    print(solr_query)
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


@app.get('/api/team/{abbreviation}',response_class=PrettyJSONResponse)
async def get_team(abbreviation: str):
    solr_query = f"http://localhost:8983/solr/teams/query?&q=abbreviation:{abbreviation}&q.op=OR&indent=true&fl=*,%5Bchild%5D&useParams="
    results = await async_request(solr_query)
    teams = results['response']['docs']
    return teams[0] if teams else {}

@app.get('/api/player/{name}',response_class=PrettyJSONResponse)
async def get_player(name: str):
    solr_query = f"http://localhost:8983/solr/players/query?q=name:%22{quote(name)}%22&q.op=OR&indent=true&fl=*,%5Bchild%5D&useParams="
    results = await async_request(solr_query)
    players = results['response']['docs']
    return players[0] if players else {}



@app.get('/api/team/{abbreviation}/search',response_class=PrettyJSONResponse)
async def search_team_articles(abbreviation: str,query: str = '',start:int=0,rows:int=10):
    articles_results,numFound = await query_articles(query,abbreviation,None,start,rows)
    return  {
            "numFound": numFound,
            "results":articles_results
        }
    
    
@app.get('/api/player/{name}/search',response_class=PrettyJSONResponse)
async def search_player_articles(name: str,query: str = '',start:int=0,rows:int=10):
    articles_results,numFound = await query_articles(query,None,name,start,rows)
    return  {
            "numFound": numFound,
            "results":articles_results
        }


@app.get('/api/search',response_class=PrettyJSONResponse)
async def search_articles(query: str = '',start:int=0,rows:int=10):
    teams_results, players_results, (articles_results,numFound) = await asyncio.gather(
        query_teams(query),
        query_players(query),
        query_articles(query,None,None,start,rows)
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
