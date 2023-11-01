from __future__ import print_function

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from d_post_params import COLUMN_INDEX_NAME, COLUMN_INDEX_MAJOR
from d_post_params import COLUMN_INDICES
from d_post_params import HEADER_ROW_INDEX

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

        # Fetch the first row which usually contains the headers
        header_row = values[0] if values else []

        # If a header row exists
        if header_row:
            # Get headers based on the specified indices and the available header columns
            dynamic_headers = [header_row[i] for i in COLUMN_INDICES if i < len(header_row)]
        
            # Print dynamically generated header
            print(', '.join(dynamic_headers))

            # Iterate through rows starting from the second row to skip the header row
            for row in values[1:]:
                # Check if the row has enough columns as specified by COLUMN_INDICES
                if len(row) >= max(COLUMN_INDICES) + 1:
                     # Get and print values for specified indices
                    row_values = [row[i] for i in COLUMN_INDICES]
                    print(', '.join(row_values) + '\n')
                else:
                    print('Insufficient columns in the row')
        else:
            print("No header row found.")

        print('\n\nData retrieval successful.')  # Display success message
    except HttpError as err:
        print(f'An error occurred: {err}')  # Display error message if HTTP request fails

if __name__ == '__main__':
    main()
