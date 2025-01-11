from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv
import time

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service("path/to/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def fetch_dynamic_content(url, driver):
    driver.get(url)
    time.sleep(5)
    return driver.page_source

def parse_headlines(page_source):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    headlines = []

    for headline in soup.select('h3'):
        text = headline.get_text(strip=True)
        if text:
            headlines.append(text)
    return headlines

def save_to_csv(data, filename):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Headline'])
            for item in data:
                writer.writerow([item])
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data: {e}")

def main():
    url = "https://www.independent.co.uk/news/world/americas/crime/arson-kenneth-fire-flamethrower-la-wildfires-california-b2677196.html" #put your url here
    print(f"Fetching data from {url}...")

    driver = setup_driver()
    try:
        page_source = fetch_dynamic_content(url, driver)
        print("Parsing content...")
        headlines = parse_headlines(page_source)

        if headlines:
            print(f"Found {len(headlines)} headlines. Saving to CSV...")
            save_to_csv(headlines, "dynamic_headlines.csv")
        else:
            print("No headlines found.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

