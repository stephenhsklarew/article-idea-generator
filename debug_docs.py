#!/usr/bin/env python3
"""Debug script to check Google Docs extraction"""
from gmail_client import GmailClient

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

    # Get email body
    email_body = gmail._get_message_body(msg_data)
    print(f"Email body length: {len(email_body)}")
    print(f"Email body preview:\n{email_body[:500]}\n")

    # Try to extract doc ID
    doc_id = gmail._extract_google_doc_id(email_body)
    print(f"Extracted Doc ID: {doc_id}\n")

    if doc_id:
        print(f"Fetching Google Doc content...")
        content = gmail.docs_client.get_document_content(doc_id)
        print(f"Doc content length: {len(content)}")
        print(f"Doc content preview:\n{content[:500]}")
    else:
        print("❌ No Google Docs link found in email")
else:
    print("No messages found")
