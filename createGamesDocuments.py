import sqlite3
import json

def get_team_document(team_id,season_id):
    cursor.execute("""
    SELECT teams.name,teams.short_name,Url,Squad,Average_age,Foreigners,Average_Player_Value,Total_Player_Value
    FROM teams LEFT JOIN teams_stats ON teams.id=teams_stats.teams_id 
    WHERE teams.id = ? AND teams_stats.season_id = ?
    """,(team_id,season_id))
    team_name,short_name,url,nr_players,average_age,foreigners,average_player_value,total_player_value = cursor.fetchone()
    team = {
        "name":team_name,
        "abbreviation":short_name,
        "url":url,
        "nr_players":nr_players,
        "average_age":average_age,
        "foreigners":foreigners,
        "average_player_value":average_player_value,
        "total_player_value":total_player_value
    }

    cursor.execute("""
    SELECT Name, Url, Games, Goals, Assists, Yellow_Cards, Double_Yellow_Cards, Red_Cards, Minutes_Played
    FROM players_stats LEFT JOIN players ON players_stats.players_id = players.id
    WHERE players_stats.teams_id = ? AND players_stats.season_id = ?
    """,(team_id,season_id))
    players = []
    for player_db in cursor.fetchall():
        player_name, player_url, nr_games, goals, assists, yellow_cards, double_yellow_cards, red_cards, minutes_played= player_db
        players.append({"name":player_name,
                        "url":player_url,
                        "nr_games":nr_games,
                        "goals":goals,
                        "assists":assists,
                        "yellow_cards":yellow_cards,
                        "double_yellow_cards":double_yellow_cards,
                        "red_cards":red_cards,
                        "minutes_played":minutes_played})

    cursor.execute("""
    SELECT Name, Url, Games, Goals, Goals_Conceded,Clean_Sheets, Yellow_Cards, Double_Yellow_Cards, Red_Cards, Minutes_Played
    FROM goalkeepers_stats LEFT JOIN players ON goalkeepers_stats.players_id = players.id
    WHERE goalkeepers_stats.teams_id = ? AND goalkeepers_stats.season_id = ?
    """,(team_id,season_id))

    for goalkeeper_db in cursor.fetchall():
        player_name, player_url, nr_games, goals, goals_conceded, clean_sheets, yellow_cards, double_yellow_cards, red_cards, minutes_played = goalkeeper_db
        players.append({"name":player_name,
                        "url":player_url,
                        "nr_games":nr_games,
                        "goals":goals,
                        "goals_conceded":goals_conceded,
                        "clean_sheets":clean_sheets,
                        "yellow_cards":yellow_cards,
                        "double_yellow_cards":double_yellow_cards,
                        "red_cards":red_cards,
                        "minutes_played":minutes_played})
    
    team["players"] = players

    return team


# Connect to the SQLite database
conn = sqlite3.connect('news_articles.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT games.id,wk,date,home_goals,away_goals,ftr,home_team.id,away_team.id,seasons.name,seasons.id
    FROM games LEFT JOIN teams home_team on games.home_id=home_team.id LEFT JOIN teams away_team on games.away_id = away_team.id LEFT JOIN seasons on season_id = seasons.id
""")

games = []
for games_db in cursor.fetchall():
    game_id,wk,date,home_goals,away_goals,ftr,home_team_id,away_team_id,season,season_id= games_db
    game={
        "wk":wk,
        "date":date,
        "home_goals":home_goals,
        "away_goals":away_goals,
        "ftr":ftr,
        "season":season
    }

    game["home_team"] = get_team_document(home_team_id,season_id)
    game["away_team"] = get_team_document(away_team_id,season_id)
    cursor.execute("""
        SELECT title,summary,text, date, url
        FROM articles
        WHERE game_id = ?
    """,(game_id,))

    article_db = cursor.fetchone()
    article = {}
    if(article_db):
        title,summary,text, date, url = article_db
        article = {
            "title":title,
            "summary":summary,
            "text":text,
            "date": date,
            "url": url
        }

    game["article"] = article
    games.append(game)


with open("games.json", "w") as json_file:
    json.dump(games, json_file, indent=4)
