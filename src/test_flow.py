from google_sheets import GoogleSheetsInterface
from twitter_poster import TwitterPoster
import time
import webbrowser
from config import SPREADSHEET_ID

def main():
    print("1. Initializing Google Sheets...")
    sheets = GoogleSheetsInterface()
    
    spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"
    print(f"\nOpening spreadsheet: {spreadsheet_url}")
    webbrowser.open(spreadsheet_url)
    
    pending_tweets = sheets.get_pending_tweets()

    if not pending_tweets:
        print("No pending tweets found!")
        return

    next_tweet = pending_tweets[0]
    print("\n2. Getting pending tweets...")
    print("\nNext tweet to be posted:")
    print("--------------------------------------------------")
    print(f"Content: {next_tweet['content']}")
    print(f"Scheduled Time: {next_tweet['scheduled_time'] or 'Not scheduled'}")
    print("\n--------------------------------------------------")

    try:
        print("\n3. Initializing Claude...")
        twitter = TwitterPoster()
        
        tweet_url = twitter.post_tweet(next_tweet['content'])
        
        print("\nUpdating Google Sheets status...")
        sheets.update_tweet_status(next_tweet['row'], 'POSTED', tweet_url)
        
        print(f"\nTweet posted successfully!")
        print(f"Tweet URL: {tweet_url}")
    
    finally:
        if 'twitter' in locals():
            twitter.close()
        
        print(f"\nOpening spreadsheet to view results: {spreadsheet_url}")
        webbrowser.open(spreadsheet_url)

if __name__ == "__main__":
    main()