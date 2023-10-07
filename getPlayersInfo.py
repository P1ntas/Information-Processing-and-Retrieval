from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup



options = webdriver.ChromeOptions()
#options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Navigate to the Page
url = 'https://www.transfermarkt.pt/premier-league/startseite/wettbewerb/GB1/plus/?saison_id='

def getPlayerStats():
    players_info = []
    for i in range(2016,2023):
        season_url = url + str(i)
        driver.get(season_url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        # find the table with the clubs of that season 
        table = soup.find('table', class_='items')
        # find all the rows of the table with clubs
        rows = table.find_all('tr', class_=['odd','even'])
        # find all the links of the clubs
        clubs = []
        for row in rows:
            cells = row.find('td')
            club_link = cells.find('a')
            clubs.append(club_link['href'])
        players_links = getPlayersLinks(clubs)
        players_info.append(getPlayerInfo(players_links, i))
    return players_info
        
def getPlayersLinks(clubs):
    players_links = []
    for club in clubs:
        club_url = 'https://www.transfermarkt.pt' + club
        driver.get(club_url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        # find the table with the clubs of that season 
        table = soup.find('table', class_='items')
        print(club_url)
        # find all the rows of the table with clubs
        rows = table.find_all('tr', class_=['odd','even'])
        
        for row in rows:
            cells = row.find('table')
            player_link = cells.find('tr').get('data-link')
            players_links.append(player_link)

    return players_links
    
def getPlayerInfo(players_links, season):
    players_info = []
    for player_link in players_links:
        player_url = 'https://www.transfermarkt.pt' + player_link
        player_url = player_url.replace('profil', 'leistungsdatendetails')

        players_info.append(player_url)

    return players_info


links = getPlayerStats()
# remove duplicates
links = [link for season in links for link in season]

# remove duplicates
links = list(dict.fromkeys(links))



# safe links in file 
with open("players_links.txt", "w") as file:
    for link in links:
        file.write(link + "\n")



