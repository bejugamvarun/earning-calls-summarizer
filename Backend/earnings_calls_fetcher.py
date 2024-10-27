from dotenv import load_dotenv
import requests
import logging
import os

load_dotenv()

# Get the API key from an environment variable
API_KEY = os.getenv("API_NINJAS_KEY")
API_NINJAS_URL = "https://api.api-ninjas.com/v1/earningstranscript"


def get_earnings_call_transcript(ticker, year, quarter):
    print(f"Fetching data for {ticker} Q{quarter} {year}...")
    params = {
        'ticker': ticker,
        'year': year,
        'quarter': quarter
    }

    headers = {
        'X-Api-Key': API_KEY  # Replace with actual API key header name
    }

    response = requests.get(API_NINJAS_URL, params=params, headers=headers)
    print(response.status_code)
    logging.debug(f"Requesting data for {ticker} Q{quarter} {year}")

    if response.status_code == 200:
        data = response.json()
        # Returns the transcript if available
        return data.get("transcript", None)
    else:
        print(
            f"Error: Unable to fetch data for {ticker} Q{quarter} {year}. Status code: {response.status_code}")
        return None
