import pandas as pd 
import sqlite3
import spacy

conn = sqlite3.connect("news_articles.db")
cursor = conn.cursor()
nlp = spacy.load("en_core_web_sm")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS article_named_players (
        article_id INTEGER,
        named_player_id INTEGER,
        PRIMARY KEY (article_id, named_player_id),
        FOREIGN KEY(article_id) REFERENCES articles(id),
        FOREIGN KEY(named_player_id) REFERENCES players(id)
    )
""")


cursor.execute("SELECT id,title FROM articles")


for row in cursor.fetchall():
    article_id, article_title = row
    doc = nlp(article_title)
    
    named_entities = [ent.text.lower() for ent in doc.ents]
    matching_players_ids = set()
    for named_entity in named_entities:
        cursor.execute("SELECT id FROM players WHERE ? LIKE '%' || Name || '%'", (named_entity,))
        matching_players_ids.update([player_id[0] for player_id in cursor.fetchall()])
    
    cursor.executemany("INSERT INTO article_named_players(article_id, named_player_id) VALUES (?, ?)", 
                        [(article_id, player_id) for player_id in matching_players_ids])
    conn.commit()