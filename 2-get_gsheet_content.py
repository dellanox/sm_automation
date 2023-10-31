import gspread
from oauth2client.service_account import ServiceAccountCredentials

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
