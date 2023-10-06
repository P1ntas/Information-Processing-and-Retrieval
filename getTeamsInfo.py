from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
from bs4 import BeautifulSoup

# Initialize a SQLite database connection
conn = sqlite3.connect("teams_stats.db")
cursor = conn.cursor()	

cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Url VARCHAR(255) NOT NULL,
        Season INT NOT NULL,
        Squad INT,
        Average_Age DOUBLE,
        Foreigners INT,
        Average_Player_Value VARCHAR(255),
        Total_Player_Value VARCHAR(255)
    )
""")


conn.commit()


options = webdriver.ChromeOptions()
#options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Navigate to the Page
url = 'https://www.transfermarkt.pt/premier-league/startseite/wettbewerb/GB1/plus/?saison_id='


def getTeamsStats():
    teams_links = []
    for i in range(2016,2024):
        season_url = url + str(i)
        driver.get(season_url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        # find the table with the clubs of that season 
        table = soup.find('table', class_='items')
        # find all the rows of the table with clubs
        rows = table.find_all('tr', class_=['odd','even'])
        # find all the links of the clubs
        clubs_stats = []
        for row in rows:
            cells = row.find('td')
            club_link = cells.find('a')
            club_stats = []
            club_stats.append('https://www.transfermarkt.pt' + club_link['href'])
            club_stats_row = club_link.find_parent('tr')
            club_stats_cells = club_stats_row.find_all('td', class_=['zentriert','rechts'])
            club_stats_cells = club_stats_cells[1:] #remove the link
            
            for stat in club_stats_cells:
                club_stats.append(stat.text)
            clubs_stats.append(club_stats)
       
        for club_stat in clubs_stats:
            cursor.execute("INSERT INTO teams (Url, Season, Squad, Average_Age, Foreigners, Average_Player_Value, Total_Player_Value) VALUES (?, ?, ?, ?, ?, ?, ?)", (club_stat[0], i, club_stat[1], club_stat[2], club_stat[3], club_stat[4], club_stat[5]))
    
    cursor.close()
    conn.commit()
    conn.close()

    return teams_links

getTeamsStats()
