from __future__ import print_function

import os.path

import subprocess
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SHEET_NAME = 'Class Data'
RANGE_NAME = 'A2:E'
SHEET_AND_RANGE_NAME = f'{SHEET_NAME}!{RANGE_NAME}'

def get_google_sheets_data():
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
            return 'No data found.'

        data = 'Name, Major:\n'
        for row in values:
            # Appending columns A and E, which correspond to indices 0 and 4.
            data += '%s, %s\n' % (row[0], row[4])
        
        return data

    except HttpError as err:
        return f"HTTP Error: {err}"

    except Exception as ex:
        return f"An error occurred: {ex}"

def call_google_sheets_api():
    google_data = get_google_sheets_data()

    if google_data:
        return f"Google Sheets data successfully fetched:\n{google_data}"
    else:
        return "No data retrieved from Google Sheets API."
