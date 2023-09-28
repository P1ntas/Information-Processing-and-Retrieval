import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to initialize a Selenium WebDriver with Chrome
def initialize_webdriver():
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")

    # Set page load strategy to 'none'
    chrome_options.set_capability("pageLoadStrategy", "eager")

    return webdriver.Chrome(options=chrome_options)


# Initialize the WebDriver
driver = initialize_webdriver()

try:
    response = requests.get("https://web.archive.org/cdx/search/cdx?url=https://www.bbc.com/sport/football/premier-league")
    # Split the data into lines
    lines = response.text.split('\n')

    lines = filter(lambda x: len(x) > 4, lines)
    # Extract and print the timestamps
    timestamps = [line.split()[1] for line in lines]

    timestamps = list(filter(lambda x: int(x) > 20160000000000, timestamps))

    timestamps.reverse()
    for timestamp in timestamps:
        # Use Selenium to wait for the page to load

        driver.get(f"https://web.archive.org/web/{timestamp}/https://www.bbc.com/sport/football/premier-league")


        regex_pattern = r'sport/football/(\d+)'

        # Page is loaded with the desired element, proceed to parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        anchors = soup.find_all('a', href=re.compile(regex_pattern))

        # Initialize a list to store the numbers found in the links
        numbers = []

        # Extract the numbers from the links and store them in the 'numbers' list
        for anchor in anchors:
            link = anchor['href']
            match = re.search(regex_pattern, link)
            if match:
                numbers.append(int(match.group(1)))

        # Print the list of numbers
        print(numbers)


finally:
    # Close the WebDriver when done
    driver.quit()
