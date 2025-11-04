#!/usr/bin/env python3
"""Debug script to see what's happening with transcript fetching"""
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import re

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def parse_subject_line(subject):
    """Parse subject line matching pattern: Notes: "Topic" MMM DD, YYYY"""
    pattern = r'^Notes:\s*"([^"]+)"\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})'
    match = re.match(pattern, subject)

    if match:
        return {
            'topic': match.group(1),
            'date': match.group(2)
        }
    return None

service = authenticate()

query = 'subject:"Notes:" from:gemini-notes@google.com'
print(f"Query: {query}\n")

results = service.users().messages().list(
    userId='me',
    q=query,
    maxResults=10
).execute()

messages = results.get('messages', [])
print(f"Found {len(messages)} messages\n")
print("=" * 80)

for idx, message in enumerate(messages, 1):
    msg_data = service.users().messages().get(
        userId='me',
        id=message['id'],
        format='full'
    ).execute()

    headers = msg_data['payload']['headers']
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')

    print(f"\n{idx}. Subject: {subject}")

    parsed = parse_subject_line(subject)
    if parsed:
        print(f"   ✓ PARSED: Topic='{parsed['topic']}', Date='{parsed['date']}'")
    else:
        print(f"   ✗ FAILED TO PARSE")
        # Try to show why
        if not subject.startswith('Notes:'):
            print(f"     - Doesn't start with 'Notes:'")
        elif '"' not in subject:
            print(f"     - No quotes found")
        else:
            print(f"     - Pattern doesn't match expected format")

    print("-" * 80)
