import signal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup

# Define a custom signal (e.g., SIGUSR1)
custom_signal = signal.SIGUSR1

# Function to handle the custom signal and gracefully exit
def custom_signal_handler(signum, frame):
    global interrupted
    interrupted = True

# Register the custom signal handler
signal.signal(custom_signal, custom_signal_handler)

options = ChromeOptions()
# options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

# Navigate to the Page
url = 'https://www.premierleague.com/news'  # Replace with your target URL
driver.get(url)

# Define a WebDriverWait with a maximum timeout (e.g., 5 seconds)
wait = WebDriverWait(driver, 5)

interrupted = False

while not interrupted:
    try:
        # Scroll down to trigger loading more content
        main_footer = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.mainFooter')))

        # Scroll down to the mainFooter
        driver.execute_script("arguments[0].scrollIntoView();", main_footer)
    except StaleElementReferenceException:
        # Handle StaleElementReferenceException and continue the loop
        continue

# Get the links
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
links = [link['href'] for link in soup.select('ul li a.media-thumbnail__link')]

# Close the headless WebDriver
driver.quit()

# Save the links to a file
with open('links.txt', 'w', encoding='utf-8') as file:
    for link in links:
        file.write(link[2:] + '\n')
