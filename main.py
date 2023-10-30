import subprocess

try:
    # Run the script that interacts with the Google Sheets API
    google_sheets_process = subprocess.Popen(['python', 'g_api.py'], stdout=subprocess.PIPE)
    google_output, _ = google_sheets_process.communicate()
    google_output = google_output.decode('utf-8')  # Decoding the byte output to string

    # If the Google Sheets API script successfully returns the desired output
    if google_output:
        # Pass the output to the script responsible for tweeting
        tweet_process = subprocess.Popen(['python', 'tweet.py', google_output], stdout=subprocess.PIPE)
        tweet_output, _ = tweet_process.communicate()
        print(tweet_output.decode('utf-8'))  # Printing the output of the tweet process
    else:
        print("Google Sheets API script did not return any data.")

except subprocess.CalledProcessError as e:
    print(f"Error in subprocess execution: {e}")

except Exception as ex:
    print(f"An error occurred: {ex}")

# Exit the program
