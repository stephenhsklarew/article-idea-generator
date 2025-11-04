#!/usr/bin/env python3
"""Test script to fetch and display transcripts without interactive prompts"""
from gmail_client import GmailClient

print("Connecting to Gmail...")
gmail = GmailClient(start_date=None)  # No date filter
print("✓ Connected\n")

print("Fetching transcripts...")
transcripts = gmail.get_transcripts()

print(f"\nFound {len(transcripts)} transcripts:\n")
print("=" * 80)

for idx, t in enumerate(transcripts, 1):
    print(f"\n{idx}. {t['topic']}")
    print(f"   Date: {t['date']}")
    print(f"   Preview: {t['body'][:150]}...")
    print("-" * 80)
