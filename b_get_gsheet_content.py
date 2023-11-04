from __future__ import print_function
import os.path

from d_post_params import COLUMN_INDICES, HEADER_ROW_INDEX, POST_CONTENT_INDEX  # Add POST_CONTENT_INDEX import
from c_credentials import SCOPES, SPREADSHEET_ID, SHEET_AND_RANGE
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
import pandas as pd

sheet_values = SHEET_AND_RANGE  # Initialize sheet_values

def get_last_processed_row():
    try:
        with open('last_processed_row.txt', 'r') as file:
            last_row = int(file.read())
    except FileNotFoundError:
        last_row = 0
    return last_row

def save_last_processed_row(row):
    with open('last_processed_row.txt', 'w') as file:
        file.write(str(row))

def concatenate_gsheet_cells(row, POST_CONTENT_INDEX, current_row):
    """
    Extracts values from the specified indexes in a single row of the sheet values,
    concatenates these values, and outputs the concatenated strings.

    Args:
    - row: A single row of values from the spreadsheet.
    - POST_CONTENT_INDEX: The indexes to retrieve values for concatenation.
    - current_row: The current row number.

    Returns:
    - concatenated_strings: A string of concatenated values.
    """
    # Assuming `ROW_INDEX` is the index representing the row/line number
    ROW_INDEX = current_row

    concatenated_values = [str(row[i]) for i in POST_CONTENT_INDEX if len(row) > i and i != ROW_INDEX]
    print(concatenated_values)

    concatenated_string = ' '.join(concatenated_values)
    return concatenated_string

       
def extract_content(row, indices):
    """
    Extracts content from specific indices in a single row of the sheet values.

    Args:
    - row: A single row of values from the spreadsheet.
    - indices: A list of indices to retrieve values from.

    Returns:
    - content: A list of content from the specified indices.
    """
    #content = [row[i] if i < len(row) else '' for i in indices]
    #return content



def main(): 
    
    #concatenated_values = [str(row[i]) for i in POST_CONTENT_INDEX if len(row) > i and i != ROW_INDEX]
    #print(concatenated_values)

    # Assuming you have the row from the spreadsheet
    #row = ['Value 1', 'Value 2', 'Value 3', 'Value 4', 'Value 5', 'Value 6', 'Value 7', 'Value 8']

    #content_values = extract_content(row, POST_CONTENT_INDEX)
    #print(content_values)
    last_row = get_last_processed_row()  # Retrieve the last processed row
    current_row = last_row + 1  # Move to the next row

    row = current_row

    concatenated_values = []
    for i in POST_CONTENT_INDEX:
        if len(row) > i and i != ROW_INDEX:
            concatenated_values.append(str(row[i]))
    print(concatenated_values)

   

    # Initialize credentials
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
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_AND_RANGE).execute()
        values = result.get('values', [])  # Values are retrieved inside the try block

        if not values:
            print('No data found.')
            return

        if current_row < len(values):
            row = values[current_row]
            concatenated_values = concatenate_gsheet_cells(row, POST_CONTENT_INDEX, current_row)
            print(f'Processed row {current_row}: {concatenated_values}')  # Do something with the concatenated content

            save_last_processed_row(current_row)  # Save the current row for the next execution

        print('\n\nData retrieval and processing successful.')

    except HttpError as err:
        print(f'An error occurred: {err}')

if __name__ == '__main__':
    main()
