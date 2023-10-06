import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Initialize a SQLite database connection
conn = sqlite3.connect("players_stats.db")
cursor = conn.cursor()	

cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Url VARCHAR(255) NOT NULL,
        Season INT NOT NULL,
        Games INT,
        Goals INT,
        Assists INT,
        Yellow_Cards INT,
        Double_Yellow_Cards INT,
        Red_Cards INT,
        Minutes_Played INT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS goalkeepers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Url VARCHAR(255) NOT NULL,
        Season INT NOT NULL,
        Games INT,
        Goals INT,
        Yellow_Cards INT,
        Double_Yellow_Cards INT,
        Red_Cards INT,
        Goals_Conceded INT,
        Clean_Sheets INT,
        Minutes_Played INT
    )
""")


conn.commit()

players_links = []

# List of links
with open("players_links.txt", "r") as file:
    for line in file:
        # Remove leading and trailing whitespace and add the link to the list
        players_links.append(line.strip())

options = webdriver.ChromeOptions()
#options.add_argument("--headless")
driver = webdriver.Chrome(options=options)


# Loop through each link and extract the player information
for i in range(0, 13):
    # Check if is a goalkeaper
    driver.get(players_links[i])
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    player_info = soup.find_all("span", class_="data-header__content")
    is_goalkeeper = False
    for info in player_info:
        if (info.text.find("Guarda-Redes") != -1):
            is_goalkeeper = True
            break
        
    
	
    table = soup.find('table', class_='items')
    premier_league_row = None
    try:
        premier_league_link = table.find('a', attrs={'title': 'Premier League'})
        premier_league_row = premier_league_link.find_parent('tr')
        premier_league_stats = premier_league_row.find_all('td', class_=['zentriert', 'rechts'])
    except AttributeError:
        pass
    if premier_league_row is not None:
        clean_premier_league_stats = []
        for stat in premier_league_stats:
            if (stat.text == '-'):
                clean_premier_league_stats.append(str(0))
            else:
                if (stat.text.find(',') != -1):
                    clean_premier_league_stats.append(stat.text)
                else:
                    clean_premier_league_stats.append(stat.text.replace('.', ''))
        premier_league_stats = clean_premier_league_stats
        
        if (is_goalkeeper and premier_league_stats[7][-1] == "'"):
            premier_league_stats[7] = premier_league_stats[7][:-1]
        elif (not is_goalkeeper and premier_league_stats[6][-1] == "'"):
            premier_league_stats[6] = premier_league_stats[6][:-1]

        if is_goalkeeper:
            cursor.execute("INSERT INTO goalkeepers (Url, Season, Games, Goals, Yellow_Cards, Double_Yellow_Cards, Red_Cards, Goals_Conceded, Clean_Sheets, Minutes_Played) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (players_links[i],int(players_links[i][-4:]), premier_league_stats[0], premier_league_stats[1], premier_league_stats[2], premier_league_stats[3], premier_league_stats[4], premier_league_stats[5], premier_league_stats[6], premier_league_stats[7]))
        else:
            cursor.execute("INSERT INTO players (Url, Season, Games, Goals, Assists, Yellow_Cards, Double_Yellow_Cards, Red_Cards, Minutes_Played) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (players_links[i], int(players_links[i][-4:]), premier_league_stats[0], premier_league_stats[1], premier_league_stats[2], premier_league_stats[3], premier_league_stats[4], premier_league_stats[5], premier_league_stats[6]))
    else:
        print("Not found")

cursor.close()
conn.commit()
conn.close()