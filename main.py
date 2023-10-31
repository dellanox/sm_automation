from spreadsheet_summary import get_spreadsheet_details
from scheduler import schedule_job
import subprocess
import sys

def print_spreadsheet_details():
    spreadsheet_info = get_spreadsheet_details()

    print(f"Spreadsheet Name: {spreadsheet_info['Spreadsheet Name']}")
    print(f"Number of Sheets: {spreadsheet_info['Number of Sheets']}")

    for sheet in spreadsheet_info['Sheet Details']:
        print(f"Sheet: {sheet['Sheet Name']} - Rows: {sheet['Rows']}")

def job():
    print("Running the spreadsheet details...")
    print_spreadsheet_details()

    try:
        # Run the script that interacts with the Google Sheets API
        g_api_process = subprocess.Popen([sys.executable, 'g_api.py'], stdout=subprocess.PIPE)
        google_output, _ = g_api_process.communicate()
        google_output = google_output.decode('utf-8')  # Decode the byte output to string

        # If the Google Sheets API script successfully returns the desired output
        if google_output:
            # Pass the output to the script responsible for tweeting
            tweet_process = subprocess.Popen([sys.executable, 'tweet.py', google_output], stdout=subprocess.PIPE)
            tweet_output, _ = tweet_process.communicate()
            print(tweet_output.decode('utf-8'))  # Print the output of the tweet process
        else:
            print("Google Sheets API script did not return any data.")

    except subprocess.CalledProcessError as e:
        print(f"Error in subprocess execution: {e}")

    except Exception as ex:
        print(f"An error occurred: {ex}")

# Call the scheduling function from scheduler.py and pass the job function and interval
schedule_job(job, 45)  # Run the job every 45 minutes
