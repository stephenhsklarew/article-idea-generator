#!/usr/bin/env python3
from gmail_client import GmailClient
import re

gmail = GmailClient(start_date=None)

results = gmail.service.users().messages().list(
    userId='me',
    q='subject:"Notes:" from:gemini-notes@google.com',
    maxResults=1
).execute()

messages = results.get('messages', [])

if messages:
    msg_data = gmail.service.users().messages().get(
        userId='me',
        id=messages[0]['id'],
        format='full'
    ).execute()

    headers = msg_data['payload']['headers']
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')

    print(f"Subject: {subject}\n")
    print("Character analysis around quotes:")
    for i, c in enumerate(subject):
        if i >= 7 and i <= 15:  # Around the first quote
            print(f"  Position {i}: '{c}' = U+{ord(c):04X} ({ord(c)})")

    print("\n" + "="*80)

    # Test current pattern
    pattern = r'^Notes:\s*["""]([^"""]+)[""]\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})'
    match = re.match(pattern, subject)

    if match:
        print(f"✓ CURRENT PATTERN MATCHED")
        print(f"  Topic: {match.group(1)}")
        print(f"  Date: {match.group(2)}")
    else:
        print(f"✗ CURRENT PATTERN DID NOT MATCH")

    # Parse with gmail_client method
    parsed = gmail.parse_subject_line(subject)
    if parsed:
        print(f"\n✓ gmail_client.parse_subject_line() worked:")
        print(f"  Topic: {parsed['topic']}")
        print(f"  Date: {parsed['date']}")
    else:
        print(f"\n✗ gmail_client.parse_subject_line() FAILED")
