import requests
from bs4 import BeautifulSoup
from utils import format_error, format_warning


def get_manga_page(url):
    """Fetch the webpage and return its content."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(format_error(f"Error fetching {url}: {e}"))
        return None


def scrape_manga_data(url):
    """Scrape the manga details from the webpage. Returns recent chapters ordered from oldest to newest."""
    html_content = get_manga_page(url)
    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")
        # Only get the first few chapter links instead of all of them
        chapter_links = soup.find_all("a", class_="chapter-name text-nowrap", limit=5)  # Limit to recent chapters
        if chapter_links:
            chapters = []
            manga_title = None
            
            # Process each chapter link
            for chapter_link in chapter_links:
                chapter_url = chapter_link.get("href")
                chapter_full_title = chapter_link.get("title")
                
                # Get manga title from the first chapter
                if chapter_full_title and not manga_title:
                    title_parts = chapter_full_title.split(" Chapter ")
                    manga_title = title_parts[0] if title_parts else chapter_full_title
                
                chapter_text = chapter_link.text.strip()
                try:
                    # Extract chapter number from the text
                    # First try to find "Chapter X" pattern
                    if "Chapter" in chapter_text:
                        chapter_parts = chapter_text.split("Chapter ")
                        if len(chapter_parts) > 1:
                            # Take everything after "Chapter " and before any non-numeric character
                            number_str = ""
                            for char in chapter_parts[1]:
                                if char.isdigit() or char == '.':
                                    number_str += char
                                else:
                                    break
                            if number_str:
                                chapter_number = float(number_str)
                                chapters.append((chapter_url, manga_title or "Title not found", chapter_text, chapter_number))
                            else:
                                print(format_warning(f"Could not extract chapter number from: {chapter_text}"))
                                continue
                    else:
                        # Fallback to direct conversion if no "Chapter" keyword
                        chapter_number = float(chapter_text)
                        chapters.append((chapter_url, manga_title or "Title not found", chapter_text, chapter_number))
                except ValueError:
                    print(format_warning(f"Skipping chapter with non-numeric text: {chapter_text}"))
                    continue
            
            # Sort chapters by number in ascending order (oldest to newest)
            chapters.sort(key=lambda x: x[3])
            return chapters
            
        else:
            print(format_error("Chapter links not found"))
            return [(url, "Chapter link not found", "", 0)]
    else:
        print(format_error("Failed to fetch page content"))
        return [(url, "Failed to fetch", "", 0)]
