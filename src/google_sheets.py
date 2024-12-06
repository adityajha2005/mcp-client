from google.oauth2 import service_account
from googleapiclient.discovery import build

class GoogleSheetsInterface:
    def __init__(self):
        self.service = None
        self._authenticate()

    def _authenticate(self):
        # Create credentials using your service account file
        credentials = service_account.Credentials.from_service_account_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        # Use these credentials to create the sheets service
        self.service = build('sheets', 'v4', credentials=credentials) 