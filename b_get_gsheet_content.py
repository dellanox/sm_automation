from __future__ import print_function

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from c_credentials import SCOPES, SPREADSHEET_ID, SHEET_NAME, RANGE_NAME, SHEET_AND_RANGE_NAME

def main():
    """
    Main function to read data from a Google Sheet.
    """
    # Load credentials from token.json or authenticate the user
    creds = None
    if os.path.exists('token.json'):
        # Load credentials from an existing token
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh the credentials if expired
            creds.refresh(Request())
        else:
            # Authenticate user if token doesn't exist or is invalid
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the new token in token.json
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Build the service with authenticated credentials
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        # Fetch values from the specified range in the spreadsheet
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_AND_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')  # Display if no data is available
            return

        print('Name, Major:')
        for row in values:
            if len(row) >= 5:  # Check if enough columns are available
                # Print columns A and E (indices 0 and 4)
                print('%s, %s' % (row[0], row[4]))
            else:
                print('Insufficient columns in the row')  # Display if columns are insufficient
        print('Name, Major:')
        for row in values:
            if len(row) >= max(COLUMN_INDEX_NAME, COLUMN_INDEX_MAJOR) + 1:
                # Print using dynamically retrieved column indices
                print('%s, %s' % (row[COLUMN_INDEX_NAME], row[COLUMN_INDEX_MAJOR]))
            else:
                print('Insufficient columns in the row') # Display if columns are insufficient

        print('\n\nData retrieval successful.')  # Display success message
    except HttpError as err:
        print(f'An error occurred: {err}')  # Display error message if HTTP request fails

if __name__ == '__main__':
    main()
