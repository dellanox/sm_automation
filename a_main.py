from __future__ import print_function

import os.path

from b_get_gsheet_content import fetch_sheet_data

def call_google_sheets_api():
    """
    Initiates a call to retrieve data from Google Sheets API.

    Returns:
        str: Success message with fetched Google Sheets data or failure message.
    """
    google_data = fetch_sheet_data()

    if google_data:
        return f"Google Sheets data successfully fetched:\n{google_data}"
    else:
        return "No data retrieved from Google Sheets API."

if __name__ == '__main__':
    # Fetch data from Google Sheets
    result = call_google_sheets_api()

    # Display the result after attempting to fetch data from Google Sheets
    print(result)
