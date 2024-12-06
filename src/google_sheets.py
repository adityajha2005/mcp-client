from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
from config import *

class GoogleSheetsInterface:
    def __init__(self):
        self.service = None
        self._authenticate()

    def _authenticate(self):
        credentials = service_account.Credentials.from_service_account_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        self.service = build('sheets', 'v4', credentials=credentials)

    def get_pending_tweets(self):
        result = self.service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Sheet1!A2:E'
        ).execute()
        
        rows = result.get('values', [])
        pending_tweets = []
        
        for row_idx, row in enumerate(rows, start=2):
            if len(row) <= COL_STATUS or row[COL_STATUS] != 'POSTED':
                tweet_data = {
                    'content': row[COL_TWEET_CONTENT],
                    'scheduled_time': row[COL_SCHEDULED_TIME] if len(row) > COL_SCHEDULED_TIME else None,
                    'row': row_idx
                }
                pending_tweets.append(tweet_data)
        
        return pending_tweets

    def update_tweet_status(self, row, status, tweet_url=None):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        values = [[status, now, tweet_url if tweet_url else '']]
        
        self.service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f'Sheet1!C{row}:E{row}',
            valueInputOption='USER_ENTERED',
            body={'values': values}
        ).execute()