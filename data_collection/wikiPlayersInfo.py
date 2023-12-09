import wikipedia
from bs4 import BeautifulSoup
import sqlite3

# open datavase connection
conn = sqlite3.connect("news_articles.db")
cursor = conn.cursor()

cursor.execute("""
    ALTER TABLE players
    ADD COLUMN summary TEXT
""")

cursor.execute("""
    ALTER TABLE players
    ADD COLUMN image_url TEXT
""")

# iterate over the players in the database 

cursor.execute("""
    SELECT id, name FROM players
""")
players = cursor.fetchall()

for player in players:
    # get the summary from wikipedia
    print(player[1])
    try:
        summary = wikipedia.summary(player[1], auto_suggest=False)
    except:
        summary = ""
    # get the image url from wikipedia
    try:
        soup = BeautifulSoup(wikipedia.WikipediaPage(player[1]).html(), 'html.parser')
        image_box = soup.find('td', class_='infobox-image')
        image = image_box.find('img')['src']
    except:
        image = ""
    # update the database
    cursor.execute("""
        UPDATE players
        SET summary = ?,
            image_url = ?
        WHERE id = ?
    """, (summary, image, player[0]))


conn.commit()
conn.close()


