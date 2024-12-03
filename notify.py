import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle
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
            flow = InstalledAppFlow.from_client_secrets_file(SHEET_CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=8080)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)
    return service


def notify_new_chapter(chapter_title, chapter_url, to_email):
    subject = f"New Chapter Alert: {chapter_title}"
    message = f"A new chapter is available now!\n\nTitle: {chapter_title}\nRead here: {chapter_url}"
    send_email(subject, message, to_email)
