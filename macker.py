import os
import gspread
from google.oauth2.service_account import Credentials
import tempfile
import config

# Dynamically load configuration from environment variables or fallback to config.py
SERVICE_KEY = os.getenv("SERVICE_KEY", config.SERVICE_KEY)
SPREAD_SHEET = os.getenv("SPREAD_SHEET", config.SPREAD_SHEET)


def initialize_sheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    # Handle credentials as a file path or environment variable content
    if os.path.isfile(SERVICE_KEY):
        # Local file path
        creds = Credentials.from_service_account_file(SERVICE_KEY, scopes=scope)
    else:
        # Assume SERVICE_KEY contains JSON content
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write(SERVICE_KEY)
            temp_file_path = temp_file.name
        creds = Credentials.from_service_account_file(temp_file_path, scopes=scope)
        os.unlink(temp_file_path)

    client = gspread.authorize(creds)
    return client.open(SPREAD_SHEET).sheet1


def add_or_update_manga(url, manga_details, to_email):
    sheet = initialize_sheet()
    try:
        cell = sheet.find(url)  # Try to find the cell with the URL
        if cell:
            row = cell.row
            # Update existing row with new manga details
            sheet.update(
                f"A{row}:D{row}",
                [[url, manga_details[1], manga_details[2], manga_details[0]]],
            )
            print(f"Updated manga at row {row}: {url}")
        else:
            # Append a new row if URL not found
            sheet.append_row(
                [url, manga_details[1], manga_details[2], manga_details[0]]
            )
            print(f"Added new manga: {url}")
    except gspread.exceptions.APIError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
