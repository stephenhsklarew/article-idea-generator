#!/usr/bin/env python3
"""Diagnostic script to check for Notes emails from Gemini"""
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate():
    """Authenticate with Gmail API"""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def check_notes_emails():
    """Check for emails with 'Notes:' in subject from Gemini"""
    service = authenticate()

    print("\n" + "="*80)
    print("CHECKING FOR 'NOTES:' EMAILS FROM GEMINI")
    print("="*80 + "\n")

    try:
        # Search for emails with "Notes:" in subject
        results = service.users().messages().list(
            userId='me',
            q='subject:"Notes:"',
            maxResults=20
        ).execute()

        messages = results.get('messages', [])

        if not messages:
            print("❌ No emails found with 'Notes:' in the subject line.\n")
            return

        print(f"✓ Found {len(messages)} emails with 'Notes:' in subject\n")
        print("-" * 80)

        for idx, message in enumerate(messages, 1):
            msg_data = service.users().messages().get(
                userId='me',
                id=message['id'],
                format='full'
            ).execute()

            headers = msg_data['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')

            print(f"\n📧 Email {idx}:")
            print(f"   From: {sender}")
            print(f"   Subject: {subject}")
            print(f"   Date: {date}")

            # Check if from Gemini
            if 'gemini' in sender.lower():
                print("   ✓ FROM GEMINI")
            else:
                print("   ⚠️  NOT from Gemini")

            print("-" * 80)

        # Now check specifically for emails from Gemini
        print("\n\n" + "="*80)
        print("CHECKING SPECIFICALLY FOR EMAILS FROM GEMINI")
        print("="*80 + "\n")

        results = service.users().messages().list(
            userId='me',
            q='from:gemini',
            maxResults=20
        ).execute()

        gemini_messages = results.get('messages', [])

        if not gemini_messages:
            print("❌ No emails found from 'Gemini'.\n")
            print("Try searching your Gmail for emails from Gemini to find the exact sender address.\n")
        else:
            print(f"✓ Found {len(gemini_messages)} emails from Gemini\n")
            print("-" * 80)

            for idx, message in enumerate(gemini_messages[:5], 1):  # Show first 5
                msg_data = service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='full'
                ).execute()

                headers = msg_data['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')

                print(f"\n📧 Gemini Email {idx}:")
                print(f"   From: {sender}")
                print(f"   Subject: {subject}")
                print("-" * 80)

    except HttpError as error:
        print(f'❌ An error occurred: {error}')

if __name__ == "__main__":
    check_notes_emails()
