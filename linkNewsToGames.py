import pandas as pd
import sqlite3
import spacy
import json



conn = sqlite3.connect("news_articles.db")
cursor = conn.cursor()
nlp = spacy.load("en_core_web_sm")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        csv_name TEXT,
        short_name TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        season_end_year INTEGER,
        wk INTEGER,
        date TEXT,
        home_id INTEGER,
        home_goals INTEGER,
        away_goals INTEGER,
        away_id INTEGER,
        ftr TEXT,
        FOREIGN KEY (home_id) REFERENCES teams(id),
        FOREIGN KEY (away_id) REFERENCES teams(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS article_named_teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id INTEGER,
        named_team_id INTEGER,
        FOREIGN KEY(article_id) REFERENCES articles(id),
        FOREIGN KEY(named_team_id) REFERENCES teams(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS team_nicknames (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_id INTEGER,
        nickname TEXT,
        FOREIGN KEY (team_id) REFERENCES teams(id)
    )
""")
cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_team_nicknames ON team_nicknames(nickname);
""")



with open("team_nicknames.json", "r") as json_file:
    teams_data = json.load(json_file)["teams"]
    for team in teams_data:
        team_name = team["name"]
        team_csv_name = team["csv_name"]
        short_name = team["short_name"]

        cursor.execute("INSERT INTO teams (name,csv_name,short_name) VALUES (?, ?, ?)",(team_name,team_csv_name,short_name ))
        team_id = cursor.lastrowid
        nicknames = [team_name.lower()] + [team_csv_name.lower()] + [nickname.lower() for nickname in team["nicknames"]]
        cursor.executemany("INSERT INTO team_nicknames (team_id, nickname) VALUES (?, ?)", [(team_id, nickname) for nickname in nicknames])
        conn.commit()


cursor.execute("SELECT id,title FROM articles")

for row in cursor.fetchall():
    article_id, article_title = row
    doc = nlp(article_title)
    
    named_entities = [ent.text.lower() for ent in doc.ents]

    for named_entity in named_entities:
        cursor.execute("SELECT team_id FROM team_nicknames WHERE ? LIKE '%' || nickname || '%'", (named_entity.lower(),))
        matching_team_ids = cursor.fetchall()
        cursor.executemany("INSERT INTO article_named_teams(article_id, named_team_id) VALUES (?, ?)", 
                            [(article_id, team_id[0]) for team_id in matching_team_ids])
        conn.commit()





game_data = pd.read_csv("premier-league-matches.csv")

filtered_game_data = game_data[game_data['Season_End_Year'] >= 2017]

for _, game_row in filtered_game_data.iterrows():
    [home_team_id,] = cursor.execute("SELECT id FROM teams WHERE csv_name = ?", (game_row['Home'],)).fetchone()
    [away_team_id,] = cursor.execute("SELECT id FROM teams WHERE csv_name = ?", (game_row['Away'],)).fetchone()
    date = game_row['Date']
    
    cursor.execute("""
        INSERT INTO games (season_end_year, wk, date, home_id, home_goals, away_goals, away_id, ftr)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (game_row['Season_End_Year'], game_row['Wk'], date,
        home_team_id, game_row['HomeGoals'], game_row['AwayGoals'], away_team_id, game_row['FTR']))
    game_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute("""SELECT DISTINCT a.id
                  FROM article_named_teams nt1
                  JOIN article_named_teams nt2 ON nt1.article_id = nt2.article_id                
                  JOIN articles a ON nt1.article_id = a.id
                  WHERE (nt1.named_team_id = ? AND nt2.named_team_id = ?) 
                  AND a.date BETWEEN DATE(?, '-7 day') AND DATE(?, '+7 day')""", 
               (home_team_id, away_team_id, date, date))

    for row in cursor.fetchall():
        (article_id,) = row
        cursor.execute("UPDATE articles SET game_id=? WHERE id=?", (game_id, article_id))
        conn.commit()

conn.close()


