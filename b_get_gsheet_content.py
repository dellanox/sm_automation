#import os

#import gspread
#from google.oauth2 import service_account
from c_credentials import SCOPES, SPREADSHEET_PARAMS  # Import SPREADSHEET_PARAMS from the credentials file
#from google.oauth2.credentials import Credentials
#from google.auth.transport.requests import Request
#from google_auth_oauthlib.flow import InstalledAppFlow
#from googleapiclient.discovery import build
#from googleapiclient.errors import HttpError


# Access the variables
spreadsheet_id = SPREADSHEET_PARAMS['SPREADSHEET_ID']
sheet_and_range = SPREADSHEET_PARAMS['SHEET_AND_RANGE_NAME']


def get_spreadsheet_details():
    """
    Fetches information about the Google Spreadsheet, such as its name,
    the number of sheets, and details for each sheet.

    Returns:
    dict: A dictionary containing details of the spreadsheet.
    """
    creds = ServiceAccountCredentials.from_json_keyfile_dict(SPREADSHEET_PARAMS, SCOPES)
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key(SPREADSHEET_PARAMS['SPREADSHEET_ID'])

    all_sheets = spreadsheet.worksheets()

    spreadsheet_details = {
        "Spreadsheet Name": spreadsheet.title,
        "Number of Sheets": len(all_sheets),
        "Sheet Details": []
    }

    for sheet in all_sheets:
        sheet_name = sheet.title
        num_rows = len(sheet.get_all_records())
        spreadsheet_details["Sheet Details"].append({"Sheet Name": sheet_name, "Rows": num_rows})

    return spreadsheet_details

def get_spreadsheet_content():
    """
    Fetches values from the specified range in the Google Spreadsheet.

    Prints the values in the specified range. If an error occurs during the operation, it prints an error message.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(SPREADSHEET_PARAMS, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_PARAMS['SPREADSHEET_ID'], range=SPREADSHEET_PARAMS['SHEET_AND_RANGE_NAME']).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        print('Name, Major:')
        for row in values:
            if len(row) >= 5:
                print('%s, %s' % (row[0], row[4]))
            else:
                print('Insufficient columns in the row')

        print('Data retrieval successful.')
    except HttpError as err:
        print(f'An error occurred: {err}')

if __name__ == '__main__':
    get_spreadsheet_content()
