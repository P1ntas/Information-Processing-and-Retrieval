import wikipedia
from bs4 import BeautifulSoup
import sqlite3

# open datavase connection
conn = sqlite3.connect("news_articles.db")
cursor = conn.cursor()

cursor.execute(""" 
    ALTER TABLE teams
    ADD COLUMN summary TEXT
""")

cursor.execute("""
    ALTER TABLE teams
    ADD COLUMN image_url TEXT
""")

# iterate over the teams in the database
cursor.execute("""
    SELECT id, name FROM teams
""")
teams = cursor.fetchall()

for team in teams:
    # get the summary from wikipedia
    print(team[1])
    try:
        summary = wikipedia.summary(team[1], auto_suggest=False)
    except:
        summary = ""
    # get the image url from wikipedia
    try:
        soup = BeautifulSoup(wikipedia.WikipediaPage(team[1]).html(), 'html.parser')
        image_box = soup.find('td', class_='infobox-image')
        image = image_box.find('img')['src']
    except:
        image = ""
    # update the database
    cursor.execute("""
        UPDATE teams
        SET summary = ?,
            image_url = ?
        WHERE id = ?
    """, (summary, image, team[0]))

conn.commit()
conn.close()