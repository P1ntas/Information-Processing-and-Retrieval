import sqlite3
import json 

conn = sqlite3.connect('news_articles.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT *
    FROM teams               
""")
final_teams = []
for team_db in cursor.fetchall():
    id, name, csv_name,short_name, summary, image_url = team_db
    team = {
        "name":name,
        "abbreviation":short_name,
        "summary":summary,
        "image_url":image_url
    }
    cursor.execute("""
        SELECT season_id, Url, Squad, Average_Age, Foreigners, Average_Player_Value, Total_Player_Value
        FROM teams_stats
        WHERE teams_id=?
    """,(id,))
    teams_stats = []
    for team_stat in cursor.fetchall():
        season_id, team_url, team_squad, team_average_age, team_foreigners, team_average_player_value, team_total_player_value = team_stat
        team_stats = {"season_id": season_id,
             "team_url": team_url,
             "team_squad": team_squad,
             "team_average_age": team_average_age.replace(',','.'),
             "team_foreigners": team_foreigners,
             "team_average_player_value": team_average_player_value,
             "team_total_player_value": team_total_player_value}
        

        cursor.execute("""
        SELECT Name, Url, Games, Goals, Assists, Yellow_Cards, Double_Yellow_Cards, Red_Cards, Minutes_Played, players.image_url
        FROM players_stats LEFT JOIN players ON players_stats.players_id = players.id
        WHERE players_stats.teams_id = ? AND players_stats.season_id = ?
        """,(id,season_id))
        players = []
        for player_db in cursor.fetchall():
            player_name, player_url, nr_games, goals, assists, yellow_cards, double_yellow_cards, red_cards, minutes_played, image_url= player_db
            players.append({"name":player_name,
                            "url":player_url,
                            "nr_games":nr_games,
                            "goals":goals,
                            "assists":assists,
                            "yellow_cards":yellow_cards,
                            "double_yellow_cards":double_yellow_cards,
                            "red_cards":red_cards,
                            "minutes_played":minutes_played,
                            "image_url":image_url})

        cursor.execute("""
        SELECT Name, Url, Games, Goals, Goals_Conceded,Clean_Sheets, Yellow_Cards, Double_Yellow_Cards, Red_Cards, Minutes_Played, players.image_url
        FROM goalkeepers_stats LEFT JOIN players ON goalkeepers_stats.players_id = players.id
        WHERE goalkeepers_stats.teams_id = ? AND goalkeepers_stats.season_id = ?
        """,(id,season_id))

        for goalkeeper_db in cursor.fetchall():
            player_name, player_url, nr_games, goals, goals_conceded, clean_sheets, yellow_cards, double_yellow_cards, red_cards, minutes_played, image_url = goalkeeper_db
            players.append({"name":player_name,
                            "url":player_url,
                            "nr_games":nr_games,
                            "goals":goals,
                            "goals_conceded":goals_conceded,
                            "clean_sheets":clean_sheets,
                            "yellow_cards":yellow_cards,
                            "double_yellow_cards":double_yellow_cards,
                            "red_cards":red_cards,
                            "minutes_played":minutes_played,
                            "image_url":image_url})
        


        team_stats["players"] = players
        teams_stats.append(team_stats)

    team["team_stats"] = teams_stats
    final_teams.append(team)
    
with open("../documents/teams.json", "w") as json_file:
    json.dump(final_teams, json_file, indent=4)

    



