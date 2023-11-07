import sqlite3
import sys
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup

# Initialize a SQLite database connection
conn = sqlite3.connect("news_articles.db")
cursor = conn.cursor()	

cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Url VARCHAR(255) NOT NULL,
        Name VARCHAR(255)
    )
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS players_stats (
        players_id INTEGER REFERENCES players(id),
        season_id INTEGER REFERENCES seasons(id),
        teams_id INTEGER REFERENCES teams(id),
        Games INT,
        Goals INT,
        Assists INT,
        Yellow_Cards INT,
        Double_Yellow_Cards INT,
        Red_Cards INT,
        Minutes_Played INT,
        PRIMARY KEY (players_id, season_id, teams_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS goalkeepers_stats (
        players_id INTEGER REFERENCES players(id),
        season_id INTEGER REFERENCES seasons(id),
        teams_id INTEGER REFERENCES teams(id),
        Games INT,
        Goals INT,
        Yellow_Cards INT,
        Double_Yellow_Cards INT,
        Red_Cards INT,
        Goals_Conceded INT,
        Clean_Sheets INT,
        Minutes_Played INT,
        PRIMARY KEY (players_id, season_id, teams_id)
    )
""")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.4567.89 Safari/537.36"
}

conn.commit()


players_links = []

# List of links
with open("players_links.txt", "r") as file:
    for line in file:
        # Remove leading and trailing whitespace and add the link to the list
        players_links.append(line.strip())



# Loop through each link and extract the player information
for i in range(0, len(players_links)):
    retry_delay = 1  # Initial retry delay in seconds
    max_retries = 5
    for retry in range(max_retries):
        response = requests.get(players_links[i], headers=headers)
        if response.status_code == 429:  # Too Many Requests
            print(f"Received 429 Too Many Requests. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff
        elif response.status_code == 404:  # Successful response
            continue
        elif response.status_code != 200:
            break
    print(players_links[i])
    page_source = response.text
    soup = BeautifulSoup(page_source, 'html.parser')
    table = soup.find('table', class_='items')
    # try to find all the row of the table from the season 16/17 until 22/23
    try:
        rows = table.find_all('tr', class_=['odd','even'])

        for row in rows:
            #print(row)
            season_cell = row.find('td', class_='zentriert')
            season = season_cell.text.split('/')[0]
            if int(season) >= 16 and int(season) <= 22:

                #find the premier league rows 
                league_cell = row.find('td', class_='hauptlink no-border-rechts')
                if league_cell.find('img')['title'] == 'Premier League':
                    player_info = soup.find_all("span", class_="data-header__content")
                    is_goalkeeper = False

                    for info in player_info:
                        if (info.text.find("Guarda-Redes") != -1):
                            is_goalkeeper = True
                            break
                    player_stats_cell = row.find_all('td', class_=['zentriert','rechts'])
                    club = player_stats_cell[1].find('a')['title']
                    player_stats = []

                    for stat in player_stats_cell:
                        if stat.text != '-':
                            player_stats.append(stat.text)
                        else:
                            player_stats.append(0)
                    if (is_goalkeeper and player_stats[7] != 0 and player_stats[7][-1] == "'"):
                        player_stats[7] = player_stats[7][:-1]
                    elif (not is_goalkeeper and player_stats[6] != 0 and player_stats[6][-1] == "'"):
                        player_stats[6] = player_stats[6][:-1]
                 
      
                    if is_goalkeeper:
                        player_stats[4] = player_stats[4].replace('\xa0', '')
                        player_stats[4] = player_stats[4].replace('-', '0')
                    else:
                        player_stats[5] = player_stats[5].replace('\xa0', '')
                        player_stats[5] = player_stats[5].replace('-', '0')

                    player_stats[1] = club
                    
                    #remove . from the minutes played if it exists
                    if is_goalkeeper and player_stats[7] != 0 :
                        player_stats[7] = player_stats[7].replace('.', '')
                    elif not is_goalkeeper and player_stats[6] != 0:
                        player_stats[6] = player_stats[6].replace('.', '')
                    #get the team id
 
                    if club[-1] == ' ':
                        club = club[:-1]

                    cursor.execute("SELECT id FROM teams WHERE name=?", (club,))
                    team_id = cursor.fetchone()[0]
                    #get the player id
                    cursor.execute("SELECT id FROM players WHERE Url=?", (players_links[i],))
                    player_id = cursor.fetchone()

                    player_name = players_links[i].split('/')[3].replace('-', ' ').title()

                    if player_id is None:
                        cursor.execute("INSERT INTO players (Url, Name) VALUES (?, ?)", (players_links[i],str(player_name),))
                        #get the player id witch was the last added to the table
                        player_id = cursor.lastrowid
                    else:
                        player_id = player_id[0]
                   

                    if is_goalkeeper:
                        cursor.execute("INSERT INTO goalkeepers_stats (players_id, season_id, teams_id,Games, Goals, Yellow_Cards, Double_Yellow_Cards, Red_Cards, Goals_Conceded, Clean_Sheets, Minutes_Played) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (player_id, season, team_id, player_stats[2], player_stats[3], player_stats[4].split('/')[0], player_stats[4].split('/')[1], player_stats[4].split('/')[2], player_stats[5], player_stats[6], player_stats[7]))
                    else:
                        cursor.execute("INSERT INTO players_stats (players_id, season_id, teams_id,Games, Goals, Assists, Yellow_Cards, Double_Yellow_Cards, Red_Cards, Minutes_Played) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (player_id, season, team_id, player_stats[2], player_stats[3], player_stats[4],  player_stats[5].split('/')[0],  player_stats[5].split('/')[1],  player_stats[5].split('/')[2], player_stats[6]))
                    
                    

    except:
        #print the error that has caught 
        print(club)
        print("Error: ", sys.exc_info())
        continue
  


    conn.commit()


conn.close()