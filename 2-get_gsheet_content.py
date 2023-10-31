import gspread
from oauth2client.service_account import ServiceAccountCredentials

from credentials import SPREADSHEET_ID, SHEET_AND_RANGE_NAME, SCOPES
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_spreadsheet_details():
    # Define your credentials and spreadsheet information
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    # Replace SPREADSHEET_ID with the actual spreadsheet ID
    spreadsheet = client.open_by_key('YOUR_SPREADSHEET_ID')

    # Get a list of all the sheets in the spreadsheet
    all_sheets = spreadsheet.worksheets()

    spreadsheet_details = {
        "Spreadsheet Name": spreadsheet.title,
        "Number of Sheets": len(all_sheets),
        "Sheet Details": []
    }

    # Iterate through each sheet and fetch its name and the number of rows
    for sheet in all_sheets:
        sheet_name = sheet.title
        num_rows = len(sheet.get_all_records())
        spreadsheet_details["Sheet Details"].append({"Sheet Name": sheet_name, "Rows": num_rows})

    return spreadsheet_details




def get_spreadsheet_content():
    """
    Fetch values from the specified range in the spreadsheet.
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

        print('Data retrieval successful.')  # Display success message
    except HttpError as err:
        print(f'An error occurred: {err}')  # Display error message if HTTP request fails

if __name__ == '__main__':
    get_spreadsheet_content()
