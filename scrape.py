import requests
from bs4 import BeautifulSoup
from utils import format_error, format_warning


def get_manga_page(url):
    """Fetch the webpage and return its content."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(format_error(f"Error fetching {url}: {e}"))
        return None


def scrape_manga_data(url):
    """Scrape the manga details from the webpage. Returns recent chapters ordered from newest to oldest."""
    html_content = get_manga_page(url)
    if not html_content:
        print(format_error("Failed to fetch page content"))
        return [(url, "Unknown Title", "Failed to fetch", 0.0)]  # Return consistent format with float

    soup = BeautifulSoup(html_content, "html.parser")
    chapters = []

    try:
        if "natomanga.com" in url:
            # Get manga title
            manga_title = None
            title_elem = soup.find("title")
            if title_elem:
                title_parts = title_elem.text.split(" - ")
                manga_title = title_parts[0].replace("Read ", "").strip()

            chapter_list = soup.find("div", class_="chapter-list")
            if chapter_list:
                # Chapters are already ordered newest first in the HTML
                chapter_rows = chapter_list.find_all("div", class_="row")
                
                for row in chapter_rows:
                    link = row.find("a")
                    if link:
                        chapter_url = link.get("href")
                        # Ensure absolute URL
                        if not chapter_url.startswith("http"):
                            chapter_url = f"https://www.natomanga.com{chapter_url}"
                        
                        chapter_text = link.text.strip()
                        # Extract numeric chapter value
                        if "Chapter" in chapter_text:
                            number_str = chapter_text.split("Chapter")[1].strip().replace("-", ".")
                            try:
                                chapter_number = float(number_str)
                                chapters.append((chapter_url, manga_title or "Unknown Title", chapter_text, chapter_number))
                            except ValueError:
                                print(f"Skipping invalid chapter: {chapter_text}")
                
                # Return first 5 chapters (already in correct order)
                return chapters[:5] if chapters else [(url, manga_title or "Unknown Title", "No chapters found", 0.0)]
            else:
                return [(url, "Unknown Title", "Chapter list not found", 0.0)]

        else:
            # Original site format handling
            chapter_links = soup.find_all("a", class_="chapter-name text-nowrap", limit=5)
            if not chapter_links:
                return [(url, "Unknown Title", "Chapter links not found", 0.0)]

            for chapter_link in chapter_links:
                chapter_url = chapter_link.get("href")
                chapter_text = chapter_link.text.strip()
                try:
                    if "Chapter" in chapter_text:
                        number_str = ""
                        for char in chapter_text.split("Chapter ")[1]:
                            if char.isdigit() or char == '.':
                                number_str += char
                            else:
                                break
                        if number_str:
                            chapter_number = float(number_str)
                            chapters.append((chapter_url, "Unknown Title", chapter_text, chapter_number))
                    else:
                        chapter_number = float(chapter_text)
                        chapters.append((chapter_url, "Unknown Title", chapter_text, chapter_number))
                except ValueError:
                    print(format_warning(f"Skipping chapter with non-numeric text: {chapter_text}"))
                    continue

            # Sort chapters by number in descending order (newest to oldest)
            if chapters:
                chapters.sort(key=lambda x: x[3], reverse=True)
                return chapters
            else:
                return [(url, "Unknown Title", "No valid chapters", 0.0)]
    except Exception as e:
        print(format_error(f"Error processing {url}: {str(e)}"))
        return [(url, "Unknown Title", "Error processing page", 0.0)]
