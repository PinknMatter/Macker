# MACKER: Automated Manga Emailer

MACKER is an automated tool that helps manga enthusiasts stay up-to-date with their favorite series. By scraping data from [manganato.com](https://manganato.com), it tracks updates and sends notifications directly to your email. MACKER stores manga details in Google Sheets and compares the last updated chapter with the latest chapter to ensure you're always informed.

## Features

- **Automated Updates**: Scrapes manga data from manganato.com.
- **Email Notifications**: Sends an email when new chapters are available.
- **Google Sheets Integration**: Saves and tracks manga details, including URLs and chapter numbers.
- **Smart Chapter Parsing**: Intelligently extracts chapter numbers from complex titles (e.g., "Chapter 150: Season 3 End").
- **Beautiful Console Output**: Color-coded and formatted console output for better readability.
- **Easy-to-Use Commands**:
  - Check for updates: `python main.py --update`
  - Add a new manga to track: `python main.py --add URL`

## Console Output Features

The script now provides beautifully formatted console output with:
- **Purple Headers**: Major section titles
- **Green Checkmarks**: Successful operations
- **Red Crosses**: Error messages
- **Yellow Warnings**: Important notices
- **Blue Manga Titles**: Manga names
- **Cyan Info**: General status updates

Example output:
```
=== Macker Script Started at 2024-12-27 23:00:00 ===
=== Checking for New Chapters ===

ℹ Checking One Piece
URL: https://manganato.com/manga-aa951409
✓ Updated to latest chapter Chapter 1075

ℹ Checking Black Clover
! Could not extract chapter number from: Special Chapter
```

---

## Prerequisites

Before using MACKER, ensure the following are installed and configured:

1. **Python 3.8+**: Download from [python.org](https://www.python.org/).
2. **Required Libraries**:
   - Install dependencies using `pip install -r requirements.txt`.
3. **Google Sheets API Setup**:
   - Enable the Google Sheets API.
   - Download your `credentials.json` file and place it in the project directory.
4. **Gmail API Setup**:
   - Enable the Gmail API and download the Gmail credentials file.

---

## Installation

## Set up the Google Sheets API:

Place the credentials for the sheets json  file in the root of your project.

## Set up the Gmail API:

Place the credentials gmail json file in the root of your project.

---

## Configure your email and file paths in config.py:

NOTIFICATION_EMAIL = "your-email@example.com"

CREDENTIALS_SHEET = "Service key"

CREDENTIALS_GMAIL = "credentials / AUTH Credentials"

SPREAD_SHEET = "Sheets name"

All credentials file should be stored in the "Creds" folder

## 1. NOTIFICATION_EMAIL
Description: The email address where notifications about new manga chapters will be sent.
Example:

NOTIFICATION_EMAIL = "noahkornberg@gmail.com"

## 2. CREDENTIALS_SHEET
Description: The filename of the Service account key/credentials

CREDENTIALS_SHEET = "./Creds/macker-428721-78ccb1f3325e.json"

## 3. CREDENTIALS_GMAIL
Description: The filename of the Gmail credentials JSON file required for sending email notifications. This file should be set up when configuring Gmail API access.
Example:

CREDENTIALS_GMAIL = "./Creds/credentials2.json"

## 4. SPREAD_SHEET
Description: The name of the Google Spreadsheet used to store manga updates.
Example:


1. Check for Updates
To check for updates on the manga chapters you are tracking, use:


python main.py --update
2. Add a New Manga to Track
To add a new manga URL for tracking, use:


python main.py --add <MANGA_URL>


For example:


python main.py --add https://manganato.com/manga-abc123

## How It Works
Track Manga:
MACKER saves manga URLs and details in a Google Sheet.

## Scrape Updates:
The script scrapes manganato.com for the latest chapter.

## Compare Chapters:
It checks the saved chapter against the latest chapter available on the site.

## Send Notifications:
If a new chapter is available, it sends an email notification to the configured address.



---

## Example

python main.py --add https://manganato.com/manga-xyz789
Check for updates:


python main.py --update
Receive an email notification for new chapters.


---

## Runy.bat

This is set up to run the bat file to automatically check for updates you can add this to your task scheduler etc..

---

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For questions or feedback, contact: noahkornberg@gmail.com
