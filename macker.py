import gspread
from oauth2client.service_account import ServiceAccountCredentials


def initialize_sheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "macker-428721-78ccb1f3325e.json", scope
    )
    client = gspread.authorize(creds)
    return client.open(
        "Macker"
    ).sheet1  # Ensure the spreadsheet exists and is shared with the service account


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


# Make sure to handle exceptions correctly and ensure that the service account has the correct permissions
