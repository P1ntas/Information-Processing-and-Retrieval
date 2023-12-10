import sqlite3
import json


conn = sqlite3.connect('news_articles.db')
cursor = conn.cursor()

def get_player_stats_document(player_id):
    cursor.execute("""
        SELECT Games,Goals,Assists,Yellow_Cards,Double_Yellow_Cards,Red_Cards,Minutes_Played,seasons.name,teams.name,teams.short_name, teams.image_url
        FROM players_stats LEFT JOIN seasons ON season_id = seasons.id LEFT JOIN teams ON teams_id = teams.id
        WHERE players_id = ?
    """,(player_id,))
    player_stats = []
    for player_stats_db in cursor.fetchall():
        nr_games,goals,assists,yellow_cards,double_yellow_cards,red_cards,minutes_played,season,team,abbreviation, teams_image_url=player_stats_db
        player_stats.append({"nr_games":nr_games,
                             "goals":goals,
                             "assists":assists,
                             "yellow_cards":yellow_cards,
                             "double_yellow_cards":double_yellow_cards,
                             "red_cards":red_cards,
                             "minutes_played":minutes_played,
                             "season":season,
                             "team":team,
                             "abbreviation":abbreviation,
                             "teams_image_url":teams_image_url})
    cursor.execute("""
        SELECT Games,Goals,Yellow_Cards,Double_Yellow_Cards,Red_Cards,Goals_Conceded,Clean_Sheets,Minutes_Played,seasons.name,teams.name,teams.short_name, teams.image_url
        FROM goalkeepers_stats LEFT JOIN seasons ON season_id = seasons.id LEFT JOIN teams ON teams_id = teams.id
        WHERE players_id = ?
    """,(player_id,))
    for player_stats_db in cursor.fetchall():
        nr_games,goals,yellow_cards,double_yellow_cards,red_cards,goals_conceded,clean_sheets,minutes_played,season,team,abbreviation, teams_image_url=player_stats_db
        player_stats.append({"nr_games":nr_games,
                             "goals_conceded":goals_conceded,
                             "clean_sheets":clean_sheets,
                             "yellow_cards":yellow_cards,
                             "double_yellow_cards":double_yellow_cards,
                             "red_cards":red_cards,
                             "minutes_played":minutes_played,
                             "season":season,
                             "team":team,
                             "abbreviation":abbreviation,
                             "teams_image_url":teams_image_url})
        
    return player_stats


conn = sqlite3.connect('news_articles.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT id, Name, Url, summary, image_url
    FROM players
    """)
players = []
for player_db in cursor.fetchall():
    player_id, player_name, player_url, player_summary, player_image_url = player_db
    player = {"name":player_name,
              "url":player_url,
              "summary":player_summary,
              "image_url":player_image_url,
             }    
    player["player_stats"] = get_player_stats_document(player_id)
    players.append(player)

with open("../documents/players.json", "w") as json_file:
    json.dump(players, json_file, indent=4)