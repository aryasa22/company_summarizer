# Google Sheets Company Summarizer
This Python script integrates Google Sheets, OpenAI GPT, and pandas to:
1. Read a list of company names from a Google Sheet.
2. Automatically search and generate concise company summaries using GPT-4o Mini with live web search.
3. Append the generated summaries back into a separate worksheet in the same Google Sheet.

## Features
- Google Sheets Integration (via `gspread` and `google-auth`).
- Automated Summarization using OpenAI's GPT-4o Mini.
- Web Search Augmentation to ensure up-to-date and accurate results.
- Data Persistence directly into Google Sheets.
- Avoids duplicate summarizations by checking existing entries.

## Requirements
### Python Version
- Python 3.12.9 or higher

### Dependencies
Install required libraries (recomended using virtual envs):
```
pip install -r requirements.txt
```

## Setup Instructions
### 1. Google Cloud Service Account
1. Create a Google Cloud project.
2. Enable Google Sheets API and Google Drive API.
3. Create a Service Account and download the .json key file.
4. Rename the file to sheet_credentials.json (or update the script to match your filename).
5. Share the target Google Sheet with the service account email.

### 2. OpenAI API Key
1. Get your API key from [OpenAI Dashboard](https://platform.openai.com/).
2. Replace "OPENAI_API_KEY" in the script with your actual key, or store it in an environment variable.

### 3. Google Sheet Structure
The sheet must contain:
- Worksheet 1: "Companies" → contains a column company_name.
- Worksheet 2: "Summaries" → stores company_name and summary.

### 4. Update sheet_id
1. Find your Google Sheet ID from the URL:
    ```
    https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit
    ```
2. Replace `sheet_id` in the script.

## Usage
### Run the script:
```
python summarize_companies.py
```

### Script flow:
1. Reads company_name values from the "Companies" worksheet.
2. Checks "Summaries" worksheet to avoid duplicates.
3. Uses GPT-4o Mini with web search to generate structured summaries.
4. Appends results to "Summaries".
