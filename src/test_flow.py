# Since we're in the same directory as other modules now
from google_sheets import GoogleSheetsInterface
from twitter_poster import TwitterPoster
import time
import webbrowser
from config import SPREADSHEET_ID

def main():
    # First connect to Google Sheets and get pending tweets
    print("Connecting to Google Sheets...")
    sheets = GoogleSheetsInterface()
    pending_tweets = sheets.get_pending_tweets()

    if not pending_tweets:
        print("No pending tweets found!")
        return

    # Show the next tweet that will be posted
    next_tweet = pending_tweets[0]
    print("\nNext tweet to be posted:")
    print("-" * 50)
    print(f"Content: {next_tweet['content']}")
    print(f"Scheduled Time: {next_tweet['scheduled_time'] or 'Not scheduled'}")
    print("-" * 50)

    # Ask for confirmation before proceeding
    input("\nPress Enter to proceed with Twitter login...")

    # Initialize Twitter and post the tweet
    try:
        twitter = TwitterPoster()
        
        print("\nReady to post tweet!")
        input("Press Enter to post the tweet...")

        tweet_url = twitter.post_tweet(next_tweet['content'])
        
        # Update the status in Google Sheets
        print("\nUpdating Google Sheets status...")
        sheets.update_tweet_status(next_tweet['row'], 'POSTED', tweet_url)
        
        print(f"\nTweet posted successfully!")
        print(f"Tweet URL: {tweet_url}")
        
        input("\nPress Enter to close the browser...")
    
    finally:
        if 'twitter' in locals():
            twitter.close()
        
        # Open spreadsheet and tweet in browser
        spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"
        print(f"\nOpening spreadsheet: {spreadsheet_url}")
        webbrowser.open(spreadsheet_url)
        
        if 'tweet_url' in locals():
            print(f"Opening tweet: {tweet_url}")
            webbrowser.open(tweet_url)

if __name__ == "__main__":
    main()