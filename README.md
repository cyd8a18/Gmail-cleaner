# Gmail Cleaner

Python scripts for cleaning a Gmail inbox with help from OpenAI classification.

The project fetches messages from Gmail, sends compact email summaries to an OpenAI model, and applies one of three decisions for each message:

- `KEEP`: leave the message untouched
- `ARCHIVE`: remove the message from the inbox
- `DELETE`: move the message to trash, or permanently delete it if enabled

## Safety Notes

This project can modify your Gmail account.

Before running it on real email, review these settings in `main.py`:

```python
BATCH_SIZE    = 100
MAX_RESULTS   = 4000
PERMANENT_DEL = False
```

Also review this call:

```python
apply_actions(service, decisions, dry_run=False, permanent_delete=PERMANENT_DEL)
```

For a safer first run, use `dry_run=True`. That previews the decisions without changing Gmail.

Keep `PERMANENT_DEL = False` unless you are completely sure. With the default setting, deleted messages are moved to trash instead of being permanently removed.

## Project Structure

```text
.
├── actions.py           # Applies KEEP, ARCHIVE, and DELETE decisions in Gmail
├── auth_fetch.py        # Handles Gmail OAuth and fetches message summaries
├── main.py              # Entry point and batch-processing settings
├── openai_classify.py   # Sends email summaries to OpenAI for classification
└── credentials.json     # Local Google OAuth credentials, not safe to commit
```

## Requirements

- Python 3.10+
- A Google Cloud OAuth client configured for Gmail API access
- An OpenAI API key

Python packages used by the scripts:

```bash
pip install openai google-api-python-client google-auth-oauthlib google-auth
```

## Setup

1. Enable the Gmail API in Google Cloud.
2. Create an OAuth client for a desktop app.
3. Download the OAuth client file and save it as `credentials.json` in the project root.
4. Set your OpenAI API key in your shell:

```bash
setx OPENAI_API_KEY "your_api_key_here"
```

Restart your terminal after using `setx`, or set it only for the current PowerShell session:

```powershell
$env:OPENAI_API_KEY = "your_api_key_here"
```

## Usage

Run the cleaner:

```bash
python main.py
```

On the first run, a browser window opens for Google OAuth consent. After authorization, the script fetches email summaries in batches, classifies them, and applies actions.

## Classification Rules

The current classifier is intentionally aggressive:

- It keeps only clearly important messages.
- It deletes most newsletters, promotions, notifications, shopping emails, and old low-value messages.
- It archives only occasional messages with minor future value.

You can adjust the behavior by editing the prompt in `openai_classify.py`.

## Git Ignore Recommendations

Do not commit credentials, generated Python cache files, or local environment files. The `.gitignore` should include:

```gitignore
.venv/
__pycache__/
*.pyc
credentials.json
credentials*.json
```

## Disclaimer

OpenAI classification can make mistakes. Always start with `dry_run=True`, inspect the printed decisions, and only then allow the script to modify Gmail.
