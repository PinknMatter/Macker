import os
import argparse
from datetime import datetime
from macker import add_or_update_manga, initialize_sheet
from scrape import scrape_manga_data
from notify import notify_new_chapter, notify_new_chapters
from utils import (
    format_header,
    format_success,
    format_error,
    format_warning,
    format_info,
    format_manga_title,
)
import config

# Dynamically load configuration from environment variables or fallback to config.py
NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL", config.NOTIFICATION_EMAIL)

print(format_header(f"Macker Script Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))


def extract_chapter_number(chapter_text):
    if not chapter_text:
        return None
    try:
        if "Chapter" in chapter_text:
            chapter_parts = chapter_text.split("Chapter ")
            if len(chapter_parts) > 1:
                number_str = ""
                for char in chapter_parts[1]:
                    if char.isdigit() or char == '.':
                        number_str += char
                    else:
                        break
                if number_str:
                    return float(number_str)
        else:
            return float(chapter_text)
    except (ValueError, TypeError):
        pass
    return None


def check_for_updates():
    print(format_header("Checking for New Chapters"))
    sheet = initialize_sheet()
    try:
        manga_entries = sheet.get_all_records()
    except Exception as e:
        print(format_error(f"Failed to retrieve sheet data: {e}"))
        return

    for entry in manga_entries:
        url = entry.get("URL")
        if url:  # Ensure the URL is not empty
            manga_title = entry.get("Title", "Unknown Manga")
            print(f"\n{format_info(f'Checking {format_manga_title(manga_title)}')}")
            print(f"URL: {url}")
            
            chapters = scrape_manga_data(url)
            if chapters and chapters[0][1] not in ["Chapter link not found", "Failed to fetch"]:
                current_chapter = entry.get("Chapter")
                current_chapter_num = extract_chapter_number(current_chapter)
                if current_chapter_num is None:
                    print(format_warning(f"Could not extract chapter number from: {current_chapter}"))
                    continue

                # Filter chapters newer than the current one and sort them
                new_chapters = [ch for ch in chapters if extract_chapter_number(ch[2]) > current_chapter_num]
                
                if new_chapters:
                    try:
                        # Send a single notification for all new chapters
                        manga_title = new_chapters[0][1]  # Get title from first chapter
                        notify_new_chapters(manga_title, new_chapters, NOTIFICATION_EMAIL)
                        print(format_success(f"Notification sent for {len(new_chapters)} new chapter(s)"))
                        
                        # After successfully sending notification, update to the latest chapter
                        latest_chapter = new_chapters[-1]  # Get the newest chapter
                        # Create a tuple with only the required fields (url, title, chapter_text)
                        manga_details = (latest_chapter[0], latest_chapter[1], latest_chapter[2])
                        add_or_update_manga(url, manga_details, NOTIFICATION_EMAIL)
                        print(format_success(f"Updated to latest chapter {latest_chapter[2]}"))
                    except Exception as e:
                        print(format_error(f"Failed to process updates: {e}"))
                else:
                    print(format_info("No new chapters found"))
            else:
                print(format_error(f"Failed to fetch manga data"))
        else:
            print(format_warning("Encountered an empty URL, skipping"))


def add_manga(urls):
    print(format_header("Adding New Manga"))
    for url in urls:
        print(f"\n{format_info(f'Processing: {url}')}")
        chapters = scrape_manga_data(url)
        if chapters and chapters[0][1] not in ["Chapter link not found", "Failed to fetch"]:
            # Get the first chapter's details
            chapter = chapters[0]
            # Create a tuple with only the required fields (url, title, chapter_text)
            manga_details = (chapter[0], chapter[1], chapter[2])
            add_or_update_manga(url, manga_details, NOTIFICATION_EMAIL)
            print(format_success(f"Added {format_manga_title(chapter[1])}"))
        else:
            print(format_error("Failed to add manga"))


def main():
    parser = argparse.ArgumentParser(description="Manage manga chapters")
    parser.add_argument(
        "--update", help="Check for updates on manga chapters", action="store_true"
    )
    parser.add_argument(
        "--add", help="Add new manga URLs separated by commas", type=str
    )

    args = parser.parse_args()

    if args.update:
        print(format_info("Update triggered by command"))
        check_for_updates()
    elif args.add:
        urls = args.add.split(",")
        add_manga(urls)
    else:
        print(
            format_warning("No command given. Use --update to check for updates or --add 'url1,url2' to add new manga.")
        )


if __name__ == "__main__":
    print(format_header(f"Macker Script Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))
    main()
