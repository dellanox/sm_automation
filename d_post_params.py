import schedule
import time

from c_credentials import SCOPES

# Spreadsheet level parameters
SPREADSHEET_ID = '1kMahFZKLS6B_dLtLEHRPktJyp31uvBsPSVfl9hC7Dlg'
SHEET_NAME = 'sm_content' # Name of a sheet in the workbook
RANGE_NAME = 'A1:F5' # A range in the spreadsheet
SHEET_AND_RANGE_NAME = f'{SHEET_NAME}!{RANGE_NAME}'

# Parameters for post processing
COLUMN_INDEX_NAME = 0
COLUMN_INDEX_MAJOR = 4

# Parameters for post processing
HEADER_ROW_INDEX = 0  # Index of the row containing headers

# Column indices to fetch (from left to right): Name at index 0, Major at index 4
COLUMN_INDICES = [0, 2, 4]

# Column index for subject and topic
SUBJECT_INDEX = 0
TOPIC_INDEX = 4

# Indexes for post content (list of indexes to be concatenated as post content)
POST_CONTENT_INDEX = [5, 6,]  

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
