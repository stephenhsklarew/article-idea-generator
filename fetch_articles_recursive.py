#!/usr/bin/env python3
"""
Fetch and analyze writing style patterns from specific Google Docs articles
Uses recursive search to find articles in edition subfolders
"""

from google_drive_client import GoogleDriveClient
from google_docs_client import GoogleDocsClient
import json

# Articles to analyze with their edition folders
TARGET_ARTICLES = {
    "First Edition": [
        "Why This Newsletter? And Why Now?",
        "AI Readiness: Are You Truly Prepared?"
    ],
    "Fifth Edition": [
        "A Business Leader's Playbook for AI Process Innovation"
    ],
    "Seventh Edition": [
        "The AI Cold Start Problem: Strategies for Business Leaders"
    ],
    "Eighth Edition": [
        "The Future of AI-Driven Software Modernization"
    ],
    "Nineth Edition": [
        "Convenience Over Perfection: The Competitive Advantage in GenAI Adoption"
    ],
    "Eleventh Edition": [
        "90% People, 10% Technology: Why AI Fails Without Change Management"
    ]
}

FOLDER_ID = "1A9zj-FOfDEg3nKhpjoTHeOjVf2x6I_Hv"

# Edition folder IDs from the listing
EDITION_FOLDERS = {
    "First Edition": "1Fi3FCt6UqAq29V4-nyAECAs1GHYrg_G3",
    "Fifth Edition": "1uLmIo-u60jxZOCitDDVBkD_7QaPNzZI7",
    "Seventh Edition": "1RZGeh-CN4rIX0u5Ve1-tuxlxEBqPKL6j",
    "Eighth Edition": "1nClDhxhmFsss42XZ-PeG4j6z-ygBVFL9",
    "Nineth Edition": "1kKOOhXAvpRG9SMfm17agqBRkd2uuMCMQ",
    "Eleventh Edition": "1-GvNWjAhGfum4YmZtHZZjevWEXURTEWA"
}

def main():
    print("Initializing Google Drive and Docs clients...")
    drive_client = GoogleDriveClient()
    docs_client = GoogleDocsClient()

    articles_data = []

    # Search each edition folder for its articles
    for edition, article_titles in TARGET_ARTICLES.items():
        folder_id = EDITION_FOLDERS.get(edition)
        if not folder_id:
            print(f"WARNING: No folder ID for {edition}")
            continue

        print(f"\n{'='*60}")
        print(f"Searching {edition} (folder: {folder_id})")
        print(f"{'='*60}")

        # Get all docs in this edition folder
        docs_in_folder = drive_client.get_documents_in_folder(folder_id=folder_id)
        print(f"Found {len(docs_in_folder)} documents in {edition}")

        for doc in docs_in_folder:
            print(f"  - {doc['name']}")

        # Try to match each target article
        for target_title in article_titles:
            matching_doc = None

            # Look for exact or partial match
            for doc in docs_in_folder:
                if target_title.lower() in doc['name'].lower():
                    matching_doc = doc
                    break

            if matching_doc:
                print(f"\n✓ Found: {matching_doc['name']}")
                print(f"  ID: {matching_doc['id']}")
                print(f"  Fetching content...")

                # Fetch the full text content
                content = docs_client.get_plain_document_content(matching_doc['id'])

                if content:
                    print(f"  Content length: {len(content)} characters")
                    articles_data.append({
                        'title': matching_doc['name'],
                        'edition': edition,
                        'id': matching_doc['id'],
                        'content': content,
                        'modified': matching_doc['modified']
                    })
                else:
                    print(f"  WARNING: No content retrieved")
            else:
                print(f"\n✗ NOT FOUND: {target_title}")

    # Save all articles to a JSON file for analysis
    output_file = '/Users/stephensklarew/Development/Scripts/Blog idea generator/articles_for_analysis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(articles_data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*70}")
    print(f"Successfully fetched {len(articles_data)} articles")
    print(f"Articles saved to: {output_file}")
    print(f"{'='*70}")

    # Print summary
    print("\nArticles retrieved:")
    for i, article in enumerate(articles_data, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Edition: {article['edition']}")
        print(f"   Characters: {len(article['content']):,}")
        print(f"   Words: {len(article['content'].split()):,} (approx)")

if __name__ == '__main__':
    main()
