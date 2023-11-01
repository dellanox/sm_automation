import schedule
import time

# Parameters for post processing
COLUMN_INDEX_NAME = 0
COLUMN_INDEX_MAJOR = 4

# Parameters for post processing
HEADER_ROW_INDEX = 0  # Index of the row containing headers

# List of column indices to fetch (left to right): Name at index 0, Major at index 4
COLUMN_INDICES = [0, 2, 4]  

def automation():
    """
    Execute tasks related to Business Improvement: Automation
    """
    print("Business Improvement: Automation")

def data_engineering():
    """
    Execute tasks related to Data Engineering: Democratized Insights
    """
    print("Data Engineering: Democratized Insights")

# Define othergit  functions similarly...

def schedule_jobs():
    """
    Schedule jobs for various functions at different intervals.
    """
    # Function to schedule a job at a specified interval
    def schedule_job(job_func, interval):
        """
        Schedule a job function to run at a specified time interval.

        :param job_func: The function to be executed.
        :param interval: The time interval (in minutes) at which the job should be executed.
        """
        schedule.every(interval).minutes.do(job_func)

    # Schedule each function separately
    schedule_job(automation, 5)
    schedule_job(data_engineering, 10)
    # Schedule other functions with intervals...

    # Loop to keep the scheduler running
    while True:
        schedule.run_pending()
        # Introduce a delay to prevent excessive CPU usage
        time.sleep(30)