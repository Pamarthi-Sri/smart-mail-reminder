import os
import requests

# GitHub Secrets nundi files create cheyadam
if os.getenv("GMAIL_CREDENTIALS"):
    with open("credentials.json", "w", encoding="utf-8") as f:
        f.write(os.getenv("GMAIL_CREDENTIALS"))

if os.getenv("GMAIL_TOKEN"):
    with open("token.json", "w", encoding="utf-8") as f:
        f.write(os.getenv("GMAIL_TOKEN"))

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail permission
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Telegram Details from GitHub Secrets
BOT_TOKEN = os.getenv("8960482129:AAElcJqusehADIDG4hb5MCg1MwehFKpgf6Q")
CHAT_ID = os.getenv("7599193207")

# Important keywords
keywords = [
    'internship',
    'placement',
    'interview',
    'hackathon',
    'deadline',
    'exam',
    'test',
    'developer',
    'job',
    'hiring',
    'opportunity',
    'application',
    'career',
    'training',
    'full stack',
    'python',
    'software',
    'engineer'
]

# Duplicate notifications avoid cheyadaniki
sent_messages = set()


def send_telegram_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=data)

    print(response.text)


def read_emails():

    creds = None

    if os.path.exists('token.json'):

        creds = Credentials.from_authorized_user_file(
            'token.json',
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(
        userId='me',
        labelIds=['UNREAD'],
        maxResults=10
    ).execute()

    messages = results.get('messages', [])

    if not messages:
        print("No unread mails found")
        return

    for message in messages:

        msg = service.users().messages().get(
            userId='me',
            id=message['id']
        ).execute()

        headers = msg['payload']['headers']

        subject = ''
        sender = ''

        for header in headers:

            if header['name'] == 'Subject':
                subject = header['value']

            if header['name'] == 'From':
                sender = header['value']

        print("Subject:", subject)

        for word in keywords:

            if word.lower() in subject.lower():

                if subject not in sent_messages:

                    send_telegram_message(
                        f"IMPORTANT MAIL ALERT\n\n"
                        f"Subject: {subject}\n\n"
                        f"From: {sender}"
                    )

                    sent_messages.add(subject)

                    print("Important Mail Found")

                break


if __name__ == "__main__":

    print("\nChecking for new mails...\n")

    read_emails()

    print("\nCompleted Successfully\n")