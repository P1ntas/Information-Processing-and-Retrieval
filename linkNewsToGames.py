import pandas as pd
import sqlite3
import spacy
import json



conn = sqlite3.connect("news_articles.db")
cursor = conn.cursor()
nlp = spacy.load("en_core_web_sm")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Season_End_Year INTEGER,
        Wk INTEGER,
        Date TEXT,
        Home TEXT,
        HomeGoals INTEGER,
        AwayGoals INTEGER,
        Away TEXT,
        FTR TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS named_entities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id INTEGER,
        named_entity TEXT,
        FOREIGN KEY(article_id) REFERENCES articles(id)
    )
""")
cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_named_entity ON named_entities(named_entity);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS team_nicknames (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_name TEXT,
        nickname TEXT
    )
""")
cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_team_nicknames ON team_nicknames(nickname);
""")


with open("team_nicknames.json", "r") as json_file:
    teams_data = json.load(json_file)["teams"]
    for team in teams_data:
        team_name = team["name"]
        nicknames = [team_name.lower()] + [nickname.lower() for nickname in team["nicknames"]]
        cursor.executemany("INSERT INTO team_nicknames (team_name, nickname) VALUES (?, ?)", [(team_name, nickname) for nickname in nicknames])


cursor.execute("SELECT id,title FROM articles")

for row in cursor.fetchall():
    article_id, article_title = row
    doc = nlp(article_title)
    named_entities = [ent.text.lower() for ent in doc.ents]
    
    for named_entity in named_entities:
        cursor.execute("INSERT INTO named_entities (article_id, named_entity) VALUES (?, ?)",
                        (article_id, named_entity))
    conn.commit()
    


conn.commit()

game_data = pd.read_csv("premier-league-matches.csv")

filtered_game_data = game_data[game_data['Season_End_Year'] >= 2017]

for _, game_row in filtered_game_data.iterrows():
    cursor.execute("""
        INSERT INTO games (Season_End_Year, Wk, Date, Home, HomeGoals, AwayGoals, Away, FTR)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (game_row['Season_End_Year'], game_row['Wk'], game_row['Date'],
          game_row['Home'], game_row['HomeGoals'], game_row['AwayGoals'], game_row['Away'], game_row['FTR']))
    game_id = cursor.lastrowid
    conn.commit()
    cursor.execute("""SELECT DISTINCT ne1.article_id, a.title
                  FROM named_entities ne1
                  JOIN named_entities ne2 ON ne1.article_id = ne2.article_id
                  JOIN team_nicknames tn1 ON ne1.named_entity = tn1.nickname
                  JOIN team_nicknames tn2 ON ne2.named_entity = tn2.nickname
                  JOIN articles a ON ne1.article_id = a.id
                  WHERE (tn1.team_name = ? AND tn2.team_name = ?)
                  AND a.date BETWEEN DATE(?, '-7 day') AND DATE(?, '+7 day')""", 
               (game_row['Home'], game_row['Away'], game_row['Date'], game_row['Date']))

    for row in cursor.fetchall():
        article_id, article_title = row
        print(f"{game_row['Home']} vs {game_row['Away']}, Week {game_row['Wk']} {game_row['Season_End_Year']-1}-{game_row['Season_End_Year']}, {article_title}")
        cursor.execute("UPDATE articles SET game_id=? WHERE id=?", (game_id, article_id))
        conn.commit()

conn.close()


