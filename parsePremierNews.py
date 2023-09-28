import newspaper
import sqlite3
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import time

# Initialize a SQLite database connection
conn = sqlite3.connect("news_articles.db")
cursor = conn.cursor()

# Create a table to store the articles if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        summary TEXT,
        text TEXT,
        date TEXT,
        url TEXT
    )
""")
conn.commit()

links = []

# List of links
with open("links.txt", "r") as file:
    for line in file:
        # Remove leading and trailing whitespace and add the link to the list
        links.append("https://" + line.strip())


# Loop through each link and extract article information
for link in links:
    # Check if the URL already exists in the database
    cursor.execute("SELECT id FROM articles WHERE url=?", (link,))
    existing_row = cursor.fetchone()

    if existing_row:
        print(f"Article with URL '{link}' already exists in the database. Skipping...")
        continue

    # Make the HTTP request with exponential backoff
    retry_delay = 1  # Initial retry delay in seconds
    max_retries = 5
    for retry in range(max_retries):
        response = requests.get(link)
        
        if response.status_code == 429:  # Too Many Requests
            print(f"Received 429 Too Many Requests. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff
        elif response.status_code == 404:  # Successful response
            continue
        elif response.status_code != 200:
            break

    # Extract article title, summary, and publication date using BeautifulSoup
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    titleElement = soup.find('h1', class_='article-header__title')
    if titleElement:
        title = titleElement.text.strip()
    else:
        print(f"Could not extract title for URL: {link}")
        continue

    summaryElement = soup.find('h4', class_='article__summary')
    if summaryElement:
        summary = summaryElement.text.strip()
    else:
        summary = ""

    date = soup.find('span', class_='article-header__publish-date').text.strip()
    # Parse the date string into a datetime object
    date_obj = datetime.strptime(date, "%d %b %Y")
    # Convert the datetime object to the desired string format (e.g., "YYYY-MM-DD")
    formatted_date = date_obj.strftime("%Y-%m-%d")

    article_body = soup.find('div', class_='copy article__body')
    text = ""
    if article_body:
        text = article_body.get_text(separator=' ')

    # Insert the article information into the database
    cursor.execute("INSERT INTO articles (title, summary, text, date, url) VALUES (?, ?, ?, ?, ?)",
                   (title, summary, text, formatted_date, link))
    conn.commit()

# Close the database connection
conn.close()
