import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleDocsClient:
    def __init__(self, credentials_path='token.pickle'):
        """Initialize Google Docs client using existing credentials"""
        self.service = None
        self.load_credentials(credentials_path)

    def load_credentials(self, credentials_path):
        """Load credentials from pickle file"""
        if not os.path.exists(credentials_path):
            raise FileNotFoundError(
                f"Credentials file '{credentials_path}' not found. "
                "Please authenticate with Gmail first."
            )

        with open(credentials_path, 'rb') as token:
            creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open(credentials_path, 'wb') as token:
                    pickle.dump(creds, token)

        self.service = build('docs', 'v1', credentials=creds)

    def get_document_content(self, document_id: str, prefer_transcript: bool = True) -> str:
        """
        Fetch the text content from a Google Doc.
        Prefers the 'Transcript' tab if available, falls back to 'Notes' tab.

        Args:
            document_id: The ID of the Google Doc
            prefer_transcript: If True, prefer the Transcript tab over Notes tab (default: True)

        Returns:
            str: The full text content of the transcript or notes
        """
        try:
            # Get document with tabs content
            document = self.service.documents().get(
                documentId=document_id,
                includeTabsContent=True
            ).execute()

            all_content = []

            # Check if document has tabs (newer format)
            if 'tabs' in document:
                transcript_tab = None
                notes_tab = None

                # Find Transcript and Notes tabs
                for tab in document['tabs']:
                    tab_title = tab.get('tabProperties', {}).get('title', '')

                    if tab_title.lower() == 'transcript':
                        transcript_tab = tab
                    elif tab_title.lower() == 'notes':
                        notes_tab = tab

                # Prefer Transcript tab if available, otherwise use Notes tab
                selected_tab = None
                if prefer_transcript and transcript_tab:
                    selected_tab = transcript_tab
                    print(f'  → Using Transcript tab')
                elif notes_tab:
                    selected_tab = notes_tab
                    if transcript_tab:
                        print(f'  → Using Notes tab (Transcript tab exists but prefer_transcript=False)')
                    else:
                        print(f'  → Using Notes tab (no Transcript tab available)')

                if selected_tab:
                    doc_content = selected_tab.get('documentTab', {}).get('body', {}).get('content', [])
                    all_content.extend(self._extract_content_from_elements(doc_content))
                else:
                    # No Transcript or Notes tab found, use first tab
                    print(f'Warning: Neither Transcript nor Notes tab found. Available tabs:')
                    for tab in document['tabs']:
                        tab_title = tab.get('tabProperties', {}).get('title', 'Untitled')
                        print(f'  - {tab_title}')
                    print('Using first tab as fallback...')

                    first_tab = document['tabs'][0]
                    doc_content = first_tab.get('documentTab', {}).get('body', {}).get('content', [])
                    all_content.extend(self._extract_content_from_elements(doc_content))
            else:
                # Legacy format (no tabs)
                doc_content = document.get('body', {}).get('content', [])
                all_content.extend(self._extract_content_from_elements(doc_content))

            return ''.join(all_content)

        except HttpError as error:
            print(f'An error occurred fetching document {document_id}: {error}')
            return ''

    def _extract_content_from_elements(self, elements):
        """Helper method to extract text from document elements"""
        content = []

        for element in elements:
            if 'paragraph' in element:
                paragraph = element['paragraph']
                for text_run in paragraph.get('elements', []):
                    if 'textRun' in text_run:
                        content.append(text_run['textRun']['content'])
            elif 'table' in element:
                # Handle tables
                table = element['table']
                for row in table.get('tableRows', []):
                    for cell in row.get('tableCells', []):
                        for cell_element in cell.get('content', []):
                            if 'paragraph' in cell_element:
                                for text_run in cell_element['paragraph'].get('elements', []):
                                    if 'textRun' in text_run:
                                        content.append(text_run['textRun']['content'])

        return content

    def extract_doc_id_from_url(self, url: str) -> str:
        """
        Extract document ID from a Google Docs URL

        Args:
            url: Google Docs URL (e.g., https://docs.google.com/document/d/DOCUMENT_ID/edit)

        Returns:
            str: The document ID
        """
        import re
        # Pattern: /document/d/{DOCUMENT_ID}/
        match = re.search(r'/document/d/([a-zA-Z0-9-_]+)', url)
        if match:
            return match.group(1)
        return url  # Return as-is if not a URL pattern
