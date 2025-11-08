#!/usr/bin/env python3
"""
Test Google Drive access and list what's in the folder
"""

from google_drive_client import GoogleDriveClient
import json

FOLDER_ID = "1A9zj-FOfDEg3nKhpjoTHeOjVf2x6I_Hv"

def main():
    print("Initializing Google Drive client...")
    drive_client = GoogleDriveClient(folder_id=FOLDER_ID)

    print(f"\nTesting access to folder: {FOLDER_ID}")

    # Try to get all files (not just docs) in the folder
    try:
        query = f"'{FOLDER_ID}' in parents and trashed=false"
        results = drive_client.service.files().list(
            q=query,
            pageSize=100,
            fields="files(id, name, mimeType, modifiedTime)"
        ).execute()

        items = results.get('files', [])

        print(f"\nFound {len(items)} items in folder:")
        print("-" * 80)

        for item in items:
            print(f"\nName: {item['name']}")
            print(f"  ID: {item['id']}")
            print(f"  Type: {item['mimeType']}")
            print(f"  Modified: {item.get('modifiedTime', 'N/A')}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
