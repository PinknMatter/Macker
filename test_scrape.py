import requests
from bs4 import BeautifulSoup
from scrape import scrape_manga_data

test_url = "https://www.natomanga.com/manga/the-veteran-healer-is-overpowered"

chapters = scrape_manga_data(test_url)

if chapters:
    print("\nLatest Chapter Found:")
    print(f"Manga: {chapters[0][1]}")
    print(f"Chapter: {chapters[0][2]}")
    print(f"Number: {chapters[0][3]}")
    print(f"URL: {chapters[0][0]}")
else:
    print("No chapters found")
