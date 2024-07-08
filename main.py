import argparse
from datetime import datetime
from macker import add_or_update_manga, initialize_sheet
from scrape import scrape_manga_data
from notify import notify_new_chapter  # Import the notification function

print("Script started at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def check_for_updates():
    print("Checking for new chapters...")
    sheet = initialize_sheet()
    try:
        manga_entries = (
            sheet.get_all_records()
        )  # Retrieves all entries at once, reducing API calls
    except Exception as e:
        print(f"Failed to retrieve sheet data: {e}")
        return

    for entry in manga_entries:
        url = entry.get("URL")
        if url:  # Ensure the URL is not empty
            print(f"Checking {url}")
            manga_details = scrape_manga_data(url)
            if (
                manga_details[1] != "Chapter link not found"
                and manga_details[1] != "Failed to fetch"
            ):
                current_chapter = entry.get(
                    "Chapter"
                )  # Retrieve the current chapter from the sheet
                if (
                    current_chapter != manga_details[2]
                ):  # Compare the scraped chapter text with the stored chapter
                    add_or_update_manga(url, manga_details, "noahkornberg@gmail.com")
                    print(f"New chapter found and updated for {url}")
                    notify_new_chapter(
                        manga_details[1],
                        manga_details[0],
                        "noahkornberg@gmail.com",
                    )

                else:
                    print("No new chapter found.")
            else:
                print(f"Failed to update for {url}")
        else:
            print("Encountered an empty URL, skipping.")


def add_manga(urls):
    for url in urls:
        print(f"Adding new manga URL: {url}")
        manga_details = scrape_manga_data(url)
        if (
            manga_details[1] != "Chapter link not found"
            and manga_details[1] != "Failed to fetch"
        ):
            add_or_update_manga(url, manga_details, "noahkornberg@gmail.com")
            print(f"New manga added for {url}")
        else:
            print("Failed to add new manga for URL:", url)


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
        print("Update triggered by command.")
        check_for_updates()
    elif args.add:
        urls = args.add.split(",")  # Split the input string into a list of URLs
        add_manga(urls)
    else:
        print(
            "No command given. Use --update to check for updates or --add 'url1,url2' to add new manga."
        )


if __name__ == "__main__":
    print("Script started at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    main()
