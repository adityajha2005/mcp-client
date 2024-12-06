import os
from dotenv import load_dotenv

load_dotenv()

# Google Sheets Configuration
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
RANGE_NAME = 'Tweets!A2:E'  # Adjust based on your sheet structure

# Claude Desktop Configuration
CLAUDE_DESKTOP_URL = "https://www.claudedesktop.com/"

# Twitter Configuration
TWITTER_LOGIN_URL = "https://twitter.com/i/flow/login"
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')

# Sheet Column Indices
COL_TWEET_CONTENT = 0
COL_SCHEDULED_TIME = 1
COL_STATUS = 2
COL_POSTED_TIME = 3
COL_TWEET_URL = 4 