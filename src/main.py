import schedule
import time
from google_sheets import GoogleSheetsInterface
from twitter_poster import TwitterPoster
from claude_interface import ClaudeInterface
from datetime import datetime
import pytz

class MCPServer:
    def __init__(self):
        print("Initializing MCP Server...")
        self.sheets = GoogleSheetsInterface()
        self.twitter = TwitterPoster()
        self.claude = ClaudeInterface()
        print("MCP Server initialized successfully!")

    def process_pending_tweets(self):
        print("\nChecking for pending tweets...")
        pending_tweets = self.sheets.get_pending_tweets()
        
        if not pending_tweets:
            print("No pending tweets found.")
            return

        print(f"Found {len(pending_tweets)} pending tweets.")
        current_time = datetime.now(pytz.UTC)
        
        for tweet in pending_tweets:
            try:
                if tweet['scheduled_time']:
                    scheduled_time = datetime.strptime(tweet['scheduled_time'], '%Y-%m-%d %H:%M:%S')
                    scheduled_time = pytz.UTC.localize(scheduled_time)
                    
                    if scheduled_time > current_time:
                        print(f"Tweet scheduled for later: {scheduled_time}")
                        continue
                
                print(f"\nProcessing tweet: {tweet['content'][:50]}...")
                
                print("Getting Claude's suggestions...")
                improved_content = self.claude.send_message(
                    f"Please review and improve this tweet while maintaining its core message (max 280 chars): {tweet['content']}"
                )
                
                print("Posting to Twitter...")
                tweet_url = self.twitter.post_tweet(improved_content)
                
                print("Updating Google Sheet...")
                self.sheets.update_tweet_status(tweet['row'], 'POSTED', tweet_url)
                
                print(f"Successfully processed tweet! URL: {tweet_url}")
                time.sleep(60)
                
            except Exception as e:
                print(f"Error processing tweet: {str(e)}")
                self.sheets.update_tweet_status(tweet['row'], 'FAILED')

    def close(self):
        print("\nShutting down MCP Server...")
        self.twitter.close()
        self.claude.close()
        print("Shutdown complete!")

def main():
    server = MCPServer()
    server.process_pending_tweets()
    schedule.every(5).minutes.do(server.process_pending_tweets)
    
    try:
        print("\nServer running. Press Ctrl+C to stop.")
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutdown requested...")
        server.close()
        print("Goodbye!")

if __name__ == "__main__":
    main() 