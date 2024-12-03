import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import config

# Dynamically load configuration from environment variables or fallback to config.py
SERVICE_KEY = os.getenv("SERVICE_KEY", config.SERVICE_KEY)
SPREAD_SHEET = os.getenv("SPREAD_SHEET", config.SPREAD_SHEET)


def initialize_sheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_KEY, scope)
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
