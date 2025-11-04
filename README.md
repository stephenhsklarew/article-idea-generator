# Newsletter Transcript Analyzer

An interactive CLI tool that fetches Gemini conversation transcripts from Gmail and analyzes them to generate newsletter content suggestions focused on AI strategy and innovation for business leaders.

## Features

- Fetches transcripts from Gmail with subject pattern: `Notes: "[Subject]" [MMM DD, YYYY]`
- Interactive CLI for selecting and analyzing transcripts
- AI-powered content analysis using Claude API
- Generates:
  - Recommended newsletter topics
  - Key insights in bullet points
  - Notable quotes with context
- Save analysis results to markdown files
- Batch processing support

## Prerequisites

- Python 3.8 or higher
- Gmail account
- Anthropic API key
- Google Cloud project with Gmail API enabled

## Setup Instructions

### 1. Clone or Download

Navigate to the project directory:
```bash
cd newsletter-transcript-analyzer
```

### 2. Install Dependencies

Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install required packages:
```bash
pip install -r requirements.txt
```

### 3. Set Up Google Cloud APIs

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable required APIs:
   - Go to "APIs & Services" > "Library"
   - Search for and enable **"Gmail API"**
   - Search for and enable **"Google Docs API"**
   - Search for and enable **"Google Drive API"**
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as application type
   - Download the credentials JSON file
   - Save it as `credentials.json` in the project directory

### 4. Set Up Anthropic API

1. Get your Anthropic API key from [console.anthropic.com](https://console.anthropic.com/)
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and configure:
   ```
   ANTHROPIC_API_KEY=your_actual_api_key_here

   # Optional: Set a start date to only analyze transcripts from this date forward
   # Format: MMDDYYYY (e.g., 10232025 for October 23, 2025)
   # Leave blank to analyze all transcripts
   START_DATE=
   ```

### 5. Configure Date Filter (Optional)

You can filter transcripts to only show those from a specific date forward:

**Option 1: Set in .env file**
```
START_DATE=10232025
```

**Option 2: Set at runtime**
When you run the program, if no START_DATE is configured, you'll be prompted whether you want to set one.

The date format is `MMDDYYYY`:
- `10232025` = October 23, 2025
- `01152025` = January 15, 2025

This is useful for:
- Focusing on recent conversations only
- Excluding old transcripts you've already processed
- Analyzing transcripts from a specific time period

### 6. First Run Authentication

On your first run, the application will open a browser window to authenticate with Google:
1. Select your Gmail account
2. Grant permission to read emails
3. The authentication token will be saved as `token.pickle` for future use

## Usage

### Running the Application

```bash
python cli.py
```

Or make it executable:
```bash
chmod +x cli.py
./cli.py
```

### Interactive Menu Options

Once the application starts, you'll see:

1. **List of available transcripts** - Shows all emails matching the subject pattern
2. **Analysis options:**
   - Enter a number (e.g., `1`) - Analyze a specific transcript
   - Enter `all` - Analyze all transcripts sequentially
   - Enter `range` (e.g., `1-5`) - Analyze a range of transcripts
   - Enter `q` - Quit the application

3. **After each analysis:**
   - View the results in formatted markdown
   - Choose to save the analysis to a file
   - Continue to the next transcript or return to the menu

### Output Format

Each analysis includes:

```markdown
## RECOMMENDED TOPICS
1-4 specific topics that could be developed into newsletter articles

## KEY INSIGHTS
5-8 bullet points capturing the most important learnings

## NOTABLE QUOTES
3-5 impactful quotes with context
```

### Saved Files

Analysis files are automatically named:
```
analysis_[topic]_[timestamp].md
```

Example: `analysis_AI_Strategy_Implementation_20250123_143022.md`

## Project Structure

```
newsletter-transcript-analyzer/
├── cli.py                  # Main interactive CLI application
├── gmail_client.py         # Gmail API integration
├── content_analyzer.py     # Claude API integration for analysis
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variable template
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── credentials.json       # Google OAuth credentials (you provide)
├── token.pickle          # Google OAuth token (auto-generated)
└── .env                  # Your environment variables (you create)
```

## Troubleshooting

### "credentials.json not found"
Download OAuth credentials from Google Cloud Console (see step 3 in Setup).

### "ANTHROPIC_API_KEY not found"
Create a `.env` file and add your Anthropic API key (see step 4 in Setup).

### "No transcripts found"
Verify that your emails have the exact subject format:
```
Notes: "Your Topic Here" [Jan 15, 2025]
```

### Authentication issues
Delete `token.pickle` and re-run the application to re-authenticate.

### Import errors
Ensure you've activated your virtual environment and installed dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Tips for Best Results

1. **Review transcripts before analyzing** - The quality of analysis depends on the transcript quality
2. **Save important analyses** - Use the save feature to keep analyses you want to reference
3. **Batch process related topics** - Use the range feature to analyze related conversations together
4. **Refine topics** - The AI suggestions are starting points; use your editorial judgment

## Security Notes

- Never commit `credentials.json`, `token.pickle`, or `.env` to version control
- Keep your API keys secure
- The application only reads emails (readonly scope)
- Authentication tokens are stored locally

## Support

For issues related to:
- Gmail API: [Google Gmail API Documentation](https://developers.google.com/gmail/api)
- Claude API: [Anthropic Documentation](https://docs.anthropic.com/)

## License

This project is provided as-is for personal use.
