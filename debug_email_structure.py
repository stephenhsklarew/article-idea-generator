#!/usr/bin/env python3
"""Debug script to check full email structure"""
from gmail_client import GmailClient
import json

gmail = GmailClient(start_date=None)

# Fetch one email
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
    print("="*80)
    print("HEADERS:")
    print("="*80)
    for h in headers:
        print(f"{h['name']}: {h['value'][:100]}")

    print("\n" + "="*80)
    print("PAYLOAD STRUCTURE:")
    print("="*80)
    print(f"mimeType: {msg_data['payload'].get('mimeType')}")

    if 'parts' in msg_data['payload']:
        print(f"\nParts count: {len(msg_data['payload']['parts'])}\n")
        for idx, part in enumerate(msg_data['payload']['parts']):
            print(f"Part {idx}:")
            print(f"  mimeType: {part.get('mimeType')}")
            print(f"  body size: {part['body'].get('size', 0)}")
            if 'filename' in part:
                print(f"  filename: {part['filename']}")

            # Check for nested parts
            if 'parts' in part:
                print(f"  nested parts: {len(part['parts'])}")
                for sub_idx, subpart in enumerate(part['parts']):
                    print(f"    Subpart {sub_idx}:")
                    print(f"      mimeType: {subpart.get('mimeType')}")
                    print(f"      body size: {subpart['body'].get('size', 0)}")

                    # Try to find links in HTML
                    if 'text/html' in subpart.get('mimeType', ''):
                        if 'data' in subpart['body']:
                            import base64
                            html = base64.urlsafe_b64decode(subpart['body']['data']).decode('utf-8', errors='ignore')
                            if 'docs.google.com' in html:
                                print(f"      ✓ Found docs.google.com in HTML!")
                                # Extract URL
                                import re
                                urls = re.findall(r'https://docs\.google\.com/document/d/([a-zA-Z0-9-_]+)', html)
                                if urls:
                                    print(f"      Document IDs found: {urls}")
else:
    print("No messages found")
