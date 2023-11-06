from __future__ import print_function
import os.path

from d_post_params import SPREADSHEET_ID, SHEET_AND_RANGE, POST_CONTENT_INDEX, ROW_INDEX, SHEET_RANGE  
from c_credentials import SCOPES
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request

#sheet_values = SHEET_AND_RANGE  # Initialize sheet_values

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

def get_column_number(column_letter):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    col = 0
    for letter in column_letter:
        col = col * 26 + letters.index(letter) + 1
    return col

def is_cell_in_range(cell, sheet_range):
    start_cell, end_cell = sheet_range.split(':')
    start_row = int(start_cell[1:])
    end_row = int(end_cell[1:])
    start_col = get_column_number(start_cell[0])
    end_col = get_column_number(end_cell[0])
    cell_row = int(cell[1:])
    cell_col = get_column_number(cell[0])
    return start_row <= cell_row <= end_row and start_col <= cell_col <= end_col


def extract_content(row, indices):
    """
    Extracts content from specific indices in a single row of the sheet values.

    Args:
    - row: A single row of values from the spreadsheet.
    - indices: A list of indices to retrieve values from.

    Returns:
    - content: A list of content from the specified indices.
    """
    content = []
    for index in indices:
        if index < len(row):
            content.append(row[index])
        else:
            content.extend('')  # If the index is out of range, append an empty string

    return content

def concatenate_gsheet_cells(POST_CONTENT_INDEX, ROW_INDEX, SHEET_RANGE, values):
    """
    Concatenates cell values from a Google Sheet based on provided indices and range.

    Args:
    - POST_CONTENT_INDEX: List of column indices representing the cells to concatenate.
    - ROW_INDEX: The row index to process.
    - SHEET_RANGE: The range in the spreadsheet to operate within.
    - values: The data retrieved from the Google Sheet.

    Returns:
    - post_content: A string representing the concatenated cell values.
    """

    concatenated_values = []
    if is_cell_in_range(f"A{ROW_INDEX}", SHEET_RANGE):
        row_data = values[ROW_INDEX]  # Retrieve the actual row data
        content = extract_content(row_data, POST_CONTENT_INDEX)  # Extract content from specified indices
        concatenated_values.extend(content)

        # Format the concatenated values
        formatted_values = '\n'.join([str(value) for value in concatenated_values])
        post_content = formatted_values.replace('"', '').replace("'", '').replace(',', '')
        print(f"Formatted Values:\n\n{post_content}")  # Print the formatted concatenated values
        return post_content



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
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_AND_RANGE).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        if ROW_INDEX < len(values):
            row = values[ROW_INDEX]  # Fetch the specific row from the values list
            concatenate_gsheet_cells(POST_CONTENT_INDEX, ROW_INDEX, SHEET_RANGE, values)
            
            save_last_processed_row(ROW_INDEX)

       
        #print('\n\nData retrieval and processing successful.') # for debugging

    except HttpError as err:
        print(f'An error occurred: {err}')

if __name__ == '__main__':
    main()
