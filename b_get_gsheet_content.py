from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

from d_post_params import COLUMN_INDICES, HEADER_ROW_INDEX, POST_CONTENT_INDEX  # Add POST_CONTENT_INDEX import
from c_credentials import SCOPES, SPREADSHEET_ID, SHEET_AND_RANGE_NAME


sheet_values = SHEET_AND_RANGE_NAME

def concatenate_gsheet_cells(sheet_values, POST_CONTENT_INDEX):
    """
    Extracts values from the specified indexes in each row of the sheet values,
    concatenates these values, and outputs the concatenated strings.

    Args:
    - sheet_values: The values extracted from the spreadsheet.
    - POST_CONTENT_INDEX: The indexes to retrieve values for concatenation.

    Returns:
    - concatenated_strings: A list of concatenated strings.
    """
    concatenated_strings = [' '.join(' '.join(str(row[i]) for i in POST_CONTENT_INDEX if len(row) > i) for row in sheet_values)]
    return concatenated_strings

# Example usage
#result = concatenate_gsheet_cells(sheet_values, POST_CONTENT_INDEX)
#print(result)


def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_AND_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        # Use the function to concatenate values at POST_CONTENT_INDEX
        concatenated_values = concatenate_gsheet_cells(values, POST_CONTENT_INDEX)
        print(concatenated_values)

        #df_all_columns = pd.DataFrame(values)
        #print(df_all_columns)

        print('\n\nData retrieval successful.')
    except HttpError as err:
        print(f'An error occurred: {err}')

if __name__ == '__main__':
    main()
