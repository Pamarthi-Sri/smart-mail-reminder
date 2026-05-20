import os
import time
import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail permission
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Telegram Bot Details
BOT_TOKEN = "8960482129:AAElcJqusehADIDG4hb5MCg1MwehFKpgf6Q"
CHAT_ID = "7599193207"

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


# Telegram message function
def send_telegram_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=data)

    print(response.text)


# Gmail checking function
def read_emails():

    creds = None

    # token.json already unte
    if os.path.exists('token.json'):

        creds = Credentials.from_authorized_user_file(
            'token.json',
            SCOPES
        )

    # login required ayithe
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

    # Gmail service
    service = build('gmail', 'v1', credentials=creds)

    # unread mails fetch
    results = service.users().messages().list(
        userId='me',
        labelIds=['UNREAD'],
        maxResults=10
    ).execute()

    messages = results.get('messages', [])

    if not messages:

        print("No unread mails found")

    for message in messages:

        msg = service.users().messages().get(
            userId='me',
            id=message['id']
        ).execute()

        headers = msg['payload']['headers']

        subject = ''
        sender = ''

        # subject and sender extract
        for header in headers:

            if header['name'] == 'Subject':
                subject = header['value']

            if header['name'] == 'From':
                sender = header['value']

        print("Subject:", subject)

        # keyword checking
        for word in keywords:

            if word.lower() in subject.lower():

                # duplicate avoid
                if subject not in sent_messages:

                    send_telegram_message(
                        f"IMPORTANT MAIL ALERT\n\n"
                        f"Subject: {subject}\n\n"
                        f"From: {sender}"
                    )

                    sent_messages.add(subject)

                    print("Important Mail Found")

                break


# Main program
if __name__ == "__main__":

    while True:

        print("\nChecking for new mails...\n")

        read_emails()

        print("\nWaiting for 60 seconds...\n")

        time.sleep(60)