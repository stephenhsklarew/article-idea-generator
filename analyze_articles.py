#!/usr/bin/env python3
"""
Fetch and analyze writing style patterns from specific Google Docs articles
"""

from google_drive_client import GoogleDriveClient
from google_docs_client import GoogleDocsClient
import json

# Articles to analyze
TARGET_ARTICLES = [
    "Why This Newsletter? And Why Now?",
    "AI Readiness: Are You Truly Prepared?",
    "A Business Leader's Playbook for AI Process Innovation",
    "The AI Cold Start Problem: Strategies for Business Leaders",
    "The Future of AI-Driven Software Modernization",
    "Convenience Over Perfection: The Competitive Advantage in GenAI Adoption",
    "90% People, 10% Technology: Why AI Fails Without Change Management"
]

FOLDER_ID = "1A9zj-FOfDEg3nKhpjoTHeOjVf2x6I_Hv"

def main():
    print("Initializing Google Drive and Docs clients...")
    drive_client = GoogleDriveClient(folder_id=FOLDER_ID)
    docs_client = GoogleDocsClient()

    print(f"\nFetching documents from folder: {FOLDER_ID}")
    all_docs = drive_client.get_documents_in_folder(folder_id=FOLDER_ID)

    print(f"Found {len(all_docs)} documents in folder\n")

    # Match target articles with actual documents
    articles_data = []

    for target_title in TARGET_ARTICLES:
        # Find document that matches this title (partial match)
        matching_doc = None
        for doc in all_docs:
            # Check if target title is a substring of the document name (case-insensitive)
            if target_title.lower() in doc['name'].lower():
                matching_doc = doc
                break

        if matching_doc:
            print(f"Found: {matching_doc['name']}")
            print(f"  ID: {matching_doc['id']}")
            print(f"  Fetching content...")

            # Fetch the full text content
            content = docs_client.get_plain_document_content(matching_doc['id'])

            if content:
                print(f"  Content length: {len(content)} characters")
                articles_data.append({
                    'title': matching_doc['name'],
                    'id': matching_doc['id'],
                    'content': content,
                    'modified': matching_doc['modified']
                })
            else:
                print(f"  WARNING: No content retrieved")
        else:
            print(f"NOT FOUND: {target_title}")

        print()

    # Save all articles to a JSON file for analysis
    output_file = '/Users/stephensklarew/Development/Scripts/Blog idea generator/articles_for_analysis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(articles_data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"Successfully fetched {len(articles_data)} out of {len(TARGET_ARTICLES)} articles")
    print(f"Articles saved to: {output_file}")
    print(f"{'='*60}")

    # Print summary
    print("\nArticles retrieved:")
    for i, article in enumerate(articles_data, 1):
        print(f"{i}. {article['title']}")
        print(f"   - {len(article['content'])} characters")
        print(f"   - {len(article['content'].split())} words (approx)")
        print()

if __name__ == '__main__':
    main()
