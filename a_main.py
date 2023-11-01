import os

import gspread
from google.oauth2 import service_account
from c_credentials import SCOPES, SPREADSHEET_PARAMS  # Import SPREADSHEET_PARAMS from the credentials file
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from c_credentials import SPREADSHEET_PARAMS
from b_get_gsheet_content import get_spreadsheet_content


def get_google_sheets_data():
    """
    Fetches data from a Google Sheet.

    Returns:
        str: Fetched data from Google Sheets or error message if any occurred.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SPREADSHEET_PARAMS['SCOPES'])

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(SPREADSHEET_PARAMS, 'SCOPES')
            creds = flow.run_local_server(port=80)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        result = get_spreadsheet_content(creds, SPREADSHEET_PARAMS['SPREADSHEET_ID'], SPREADSHEET_PARAMS['SHEET_AND_RANGE_NAME'])

        if not result:
            return 'No data found.'

        data = 'Name, Major:\n'
        for row in result:
            data += '%s, %s\n' % (row[0], row[4])

        return data

    except HttpError as err:
        return f"HTTP Error: {err}"

    except Exception as ex:
        return f"An error occurred: {ex}"


def call_google_sheets_api():
    """
    Initiates a call to retrieve data from Google Sheets API.

    Returns:
        str: Success message with fetched Google Sheets data or failure message.
    """
    google_data = get_google_sheets_data()

    if google_data:
        return f"Google Sheets data successfully fetched:\n{google_data}"
    else:
        return "No data retrieved from Google Sheets API."


if __name__ == '__main__':
    # Fetch data from Google Sheets
    result = call_google_sheets_api()

    # Displaying the result after attempting to fetch data from Google Sheets
    print(result)

