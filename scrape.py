import requests
from bs4 import BeautifulSoup


def get_manga_page(url):
    """Fetch the webpage and return its content."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def scrape_manga_data(url):
    """Scrape the manga details from the webpage."""
    html_content = get_manga_page(url)
    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")
        chapter_link = soup.find("a", class_="chapter-name text-nowrap")
        if chapter_link:
            chapter_url = chapter_link.get("href")
            chapter_full_title = chapter_link.get("title")
            if chapter_full_title:
                # Split the title to remove chapter part if ' chapter ' exists
                title_parts = chapter_full_title.split(" Chapter ")
                manga_title = title_parts[0] if title_parts else chapter_full_title
            else:
                manga_title = "Title not found"
            chapter_text = chapter_link.text.strip()
            print(
                f"Scraped data - URL: {chapter_url}, Title: {manga_title}, Text: {chapter_text}"
            )
            return (chapter_url, manga_title, chapter_text)
        else:
            print("Chapter link not found")
            return (url, "Chapter link not found", "")
    else:
        print("Failed to fetch page content")
        return (url, "Failed to fetch", "")
