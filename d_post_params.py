import schedule
import time

# Spreadsheet level parameters
SPREADSHEET_ID = '1kMahFZKLS6B_dLtLEHRPktJyp31uvBsPSVfl9hC7Dlg'
SHEET = 'sm_content' # Name of a sheet in the workbook
SHEET_RANGE = 'A1:I21' # A range in the spreadsheet
SHEET_AND_RANGE = f'{SHEET}!{SHEET_RANGE}'


# Parameters for post processing
HEADER_ROW_INDEX = 0  # Index of the row containing headers

# Column index for subject and topic
"""Add the key=value pair for the neccessary columns in 
spreadsheet"""
SUBJECT = 3
TOPIC = 4
NICHE = 5
CONTEXT = 6
MEDIA = 7 
CONTENT = 8

# Indexes for post content (list of indexes to be concatenated as post content)
POST_CONTENT_INDEX = [TOPIC, MEDIA, CONTENT] 

ROW_INDEX = 3


# Function to retrieve unique values at a specific index
def get_unique_values(sheet_values, index):
    """Retrieve unique values at the specified index from the spreadsheet values."""
    unique_values = pd.DataFrame(sheet_values)[index].unique().tolist()
    return unique_values

# Schedule jobs function
def automation():
    print("Business Improvement: Automation")

def data_engineering():
    print("Data Engineering: Democratized Insights")

# Define other functions similarly...

def schedule_jobs():
    def schedule_job(job_func, interval):
        schedule.every(interval).minutes.do(job_func)

    schedule_job(automation, 5)
    schedule_job(data_engineering, 10)
    # Schedule other functions with intervals...

    while True:
        schedule.run_pending()
        time.sleep(30)
