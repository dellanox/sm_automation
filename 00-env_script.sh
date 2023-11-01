#!/bin/bash

# Install necessary Python packages
pip install google-auth
pip install tweepy
pip install scheduler
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install gspread


# Run the Python script
python 2-get_gsheet_content.py
