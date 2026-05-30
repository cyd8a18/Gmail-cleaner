from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64, json

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('gmail', 'v1', credentials=creds)

def fetch_emails(service, max_results=500):
    emails = []
    next_page_token = None

    while len(emails) < max_results:

        batch_size = min(500, max_results - len(emails))

        results = service.users().messages().list(
            userId='me',
            maxResults=batch_size,
            q='-in:spam -in:trash -in:sent -in:drafts',
            pageToken=next_page_token
        ).execute()

        messages = results.get('messages', [])

        if not messages:
            break

        for msg in messages:
            full = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()

            headers = {
                h['name']: h['value']
                for h in full['payload']['headers']
            }

            snippet = full.get('snippet', '')

            emails.append({
                'id': msg['id'],
                'from': headers.get('From', ''),
                'subject': headers.get('Subject', ''),
                'snippet': snippet
            })

            if len(emails) >= max_results:
                break

        next_page_token = results.get('nextPageToken')

        print(f"Fetched {len(emails)} emails...")

        if not next_page_token:
            break

    return emails