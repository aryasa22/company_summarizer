# Before you run, make sure all dependencies are installed
# pip install gspread openai google-auth pandas

# Import dependencies
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import openai


# OpenAI API Key (replace with your own)
openai.api_key = "OPENAI_API_KEY"


# Google Cloud API Scopes (permissions for Sheets and Drive)
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


# Load credentials from JSON file
# This file must contain your Google Service Account credentials
creds = Credentials.from_service_account_file("SHEET_CREDENTIALS.json", scopes=scope)

# Authenticate with Google Sheets API
client = gspread.authorize(creds)

# Google Sheet ID (replace with your own)
sheet_id = "GOOGLE_SHEET_ID"



# Function: Read Google Sheet data
def read_sheet(sheet_id: str, worksheet_name: str) -> pd.DataFrame:
    """
    Reads data from a specific worksheet in a Google Sheet and returns it as a pandas DataFrame.

    Args:
        sheet_id (str): The unique ID of the Google Sheet.
        worksheet_name (str): The name of the worksheet (tab) to read.

    Returns:
        pd.DataFrame: DataFrame containing the worksheet data, with the first row as column headers.
    """
    # Build Google Sheet URL from ID
    gsheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
    
    # Open Google Sheet by URL
    sheet = client.open_by_url(gsheet_url)

    # Select the desired worksheet
    worksheet = sheet.worksheet(worksheet_name)

    # Fetch all records (returns a list of dictionaries)
    data = worksheet.get_all_records()

    # Convert list of dictionaries to pandas DataFrame
    df = pd.DataFrame(data)

    return df



# Function: Add a row to a Google Sheet
def add_row(sheet_id: str, worksheet_name: str, row_data: list) -> bool:
    """
    Appends a new row to a specific worksheet in a Google Sheet.

    Args:
        sheet_id (str): The unique ID of the Google Sheet.
        worksheet_name (str): The name of the worksheet (tab) to update.
        row_data (list): List containing the row values to append.

    Returns:
        bool: True if the operation was successful.
    """
    # Build Google Sheet URL from ID
    gsheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
    
    # Open Google Sheet by URL
    sheet = client.open_by_url(gsheet_url)

    # Select the desired worksheet
    worksheet = sheet.worksheet(worksheet_name)

    # Append the row to the worksheet
    worksheet.append_row(row_data)

    return True



# Function: Get company summarization using OpenAI + Web Search
def get_summarization(company_name: str) -> str:
    """
    Generates a factual, concise summary of a company based on publicly available information.

    The summary includes:
    - Year Founded
    - Headquarters Location
    - Industry/Sector
    - Core Products/Services
    - Main Target Market/Customer Segment

    Args:
        company_name (str): The company's name.

    Returns:
        str: The generated company summary.
    """
    prompt = f"""Your task is to summarize what the company does based on publicly available information such as their official website, LinkedIn profile, or press releases.
The summary should be concise, factual, and written in clear, professional English. Avoid speculation and marketing jargon.
Include the following details when available:
1. Year Founded
2. Headquarters Location (City, Country)
3. Industry / Sector
4. Core Products or Services
5. Main Target Market or Customer Segment
If any information is missing, explicitly state “Not publicly available” instead of guessing.
Keep the final summary under 150 words.
COMPANY NAME: {company_name}"""
    
    # Call OpenAI API with web search tool
    response = openai.responses.create(
        model="gpt-4o-mini",
        tools=[{"type": "web_search_preview"}],
        input=prompt
    )

    return response.output_text



# Function: Summarize company data from Google Sheet
def summarize_data() -> bool:
    """
    Reads company names from the 'Companies' worksheet, generates summaries,
    and saves them into the 'Summaries' worksheet.

    The function skips companies that already have a recorded summary.

    Returns:
        bool: True if the process completes successfully.
    """
    # Fetch company names from 'Companies' sheet
    company_name_data = read_sheet(sheet_id, "Companies")    
    
    # Process each company name
    for name in company_name_data['company_name']:
        
        # Fetch already summarized companies
        summarized_companies = read_sheet(sheet_id, "Summaries")
        
        # Initialize columns if 'Summaries' sheet is empty
        if len(summarized_companies) == 0:
            summarized_companies['company_name'] = []
            summarized_companies['summary'] = []
        
        # Skip if company already has a summary
        if name in summarized_companies['company_name'].tolist():
            continue
        
        # Get summarization using OpenAI + web search
        summarized = get_summarization(name)

        # Append summary to the Google Sheet
        add_row(sheet_id, "Summaries", [name, summarized])
        print(f"Successfully summarized: {name}")
    
    return True



# Main execution block

if __name__ == "__main__":
    summarize_data()
