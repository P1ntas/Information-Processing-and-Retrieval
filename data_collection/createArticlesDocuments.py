import sqlite3
import json

# Connect to the SQLite database
conn = sqlite3.connect('news_articles.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT *
    FROM articles
""")
articles = []

for article_db in cursor.fetchall():
    id,title,summary,text, date, url, game_id = article_db
    article = {
        "id":id,
        "title":title,
        "summary":summary,
        "text":text,
        "date":f"{date}T00:00:00Z",
        "url": url
    }
    if(game_id):
        cursor.execute("""
                SELECT wk,date,home_goals,away_goals,ftr,home_team.name,away_team.name,seasons.name, home_team.image_url, away_team.image_url
                FROM games LEFT JOIN teams home_team on games.home_id=home_team.id LEFT JOIN teams away_team on games.away_id = away_team.id LEFT JOIN seasons on season_id = seasons.id
                WHERE games.id=?
            """,(game_id,))
        

        wk,date,home_goals,away_goals,ftr,home_team,away_team,season,home_team_image_url, away_team_image_url = cursor.fetchone()
        game={
            "wk":wk,
            "date":f"{date}T00:00:00Z",
            "home_goals":home_goals,
            "away_goals":away_goals,
            "ftr":ftr,
            "home_team":home_team,
            "home_team_image_url":home_team_image_url,
            "away_team":away_team,
            "away_team_image_url":away_team_image_url,
            "season": season
        }
        
        article["named_game"] = game
    else:
        article["named_game"] = {}
    
    cursor.execute("""
        SELECT name,short_name, teams.image_url
        FROM article_named_teams LEFT JOIN teams ON named_team_id = teams.id
        WHERE article_id=?
    """,(id,))

    named_teams = []
    for teams_db in cursor.fetchall():
        team_name,short_name, image_url = teams_db
        named_teams.append({"name":team_name,"abbreviation":short_name,"article_id":id,"image_url":image_url})


    article["named_teams"]=named_teams

    cursor.execute("""
        SELECT name,Url, players.image_url
        FROM article_named_players LEFT JOIN players ON named_player_id = players.id
        WHERE article_id=?
    """,(id,))

    named_players = []
    for players_db in cursor.fetchall():
        player_name,url, image_url = players_db
        named_players.append({"name":player_name,"url":url,"image_url":image_url})

    article["named_players"]=named_players
    articles.append(article)

with open("../documents/articles.json", "w") as json_file:
    json.dump(articles, json_file, indent=4)
