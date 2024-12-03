import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle
import tempfile
import config

# Dynamically load Gmail credentials
SHEET_CREDENTIALS = os.getenv("CREDENTIALS_GMAIL", config.SHEET_CREDENTIALS)


def send_email(subject, message, to_email):
    service = get_gmail_service()
    msg = MIMEMultipart()
    msg["to"] = to_email
    msg["from"] = "me"
    msg["subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    body = {"raw": raw}
    try:
        message = service.users().messages().send(userId="me", body=body).execute()
        print("Email sent! Message Id: %s" % message["id"])
    except Exception as e:
        print("An error occurred: %s" % e)


def get_gmail_service():
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Handle environment variable-based credentials
            if SHEET_CREDENTIALS.startswith("{"):
                # Assume SHEET_CREDENTIALS contains JSON content directly
                with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
                    temp_file.write(SHEET_CREDENTIALS)
                    temp_file_path = temp_file.name
            else:
                # Assume SHEET_CREDENTIALS is a file path
                temp_file_path = SHEET_CREDENTIALS

            try:
                flow = InstalledAppFlow.from_client_secrets_file(temp_file_path, SCOPES)
                creds = flow.run_local_server(port=8080)
            finally:
                # Clean up temporary file if created
                if temp_file_path != SHEET_CREDENTIALS and os.path.exists(
                    temp_file_path
                ):
                    os.unlink(temp_file_path)

        # Save the credentials for future use
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)


def notify_new_chapter(chapter_title, chapter_url, to_email):
    subject = f"New Chapter Alert: {chapter_title}"
    message = f"A new chapter is available now!\n\nTitle: {chapter_title}\nRead here: {chapter_url}"
    send_email(subject, message, to_email)
