import pandas as pd
import sqlite3
import spacy


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

    cursor.execute("""  SELECT id,title 
                        FROM articles
                        WHERE date BETWEEN DATE(?, '-7 day') AND DATE(?, '+7 day')
                    """, (game_row["Date"],game_row["Date"]))
    
    for row in cursor.fetchall():
        article_id, article_title = row
        doc = nlp(article_title)
        named_entities = set([ent.text.lower() for ent in doc.ents])
        if game_row['Home'].lower() in named_entities and game_row['Away'].lower() in named_entities:
            print(f"{game_row['Home']} vs {game_row['Away']}, Week {game_row['Wk']} {game_row['Season_End_Year']-1}-{game_row['Season_End_Year']}, {article_title}")
            cursor.execute("UPDATE articles SET game_id=? WHERE id=?", (game_id, article_id))
            conn.commit()


conn.close()
