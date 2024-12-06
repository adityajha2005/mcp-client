from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import TWITTER_USERNAME, TWITTER_PASSWORD
import time

class TwitterPoster:
    def __init__(self):
        """Initialize the Twitter poster with Chrome webdriver"""
        try:
            print("Initializing Chrome webdriver...")
            options = webdriver.ChromeOptions()
            # options.add_argument('--headless')  # Uncomment to run in headless mode
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.maximize_window()
            self._login()
        except Exception as e:
            print(f"Error initializing Twitter poster: {str(e)}")
            if hasattr(self, 'driver'):
                self.driver.quit()
            raise

    def _login(self):
        """Log into Twitter account"""
        try:
            print("Loading Twitter login page...")
            self.driver.get("https://twitter.com/login")
            
            # Wait for and enter username
            print("Waiting for username input field...")
            username_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]'))
            )
            username_input.send_keys(TWITTER_USERNAME)
            
            # Click the 'Next' button
            print("Clicking 'Next' button...")
            next_button = self.driver.find_element(By.XPATH, "//span[text()='Next']")
            next_button.click()
            
            # Wait for and enter password
            print("Waiting for password input field...")
            password_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
            )
            password_input.send_keys(TWITTER_PASSWORD)
            
            # Click the 'Log in' button
            print("Clicking 'Log in' button...")
            login_button = self.driver.find_element(By.XPATH, "//span[text()='Log in']")
            login_button.click()
            
            # Wait for login to complete
            print("Waiting for login to complete...")
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]'))
            )
            print("Successfully logged in to Twitter!")
            
        except Exception as e:
            print(f"Login failed with error: {str(e)}")
            print(f"Current URL: {self.driver.current_url}")
            print("\nDebug: Current page source:")
            print(self.driver.page_source[:1000] + "...") # Print first 1000 chars of page source
            raise

    def post_tweet(self, content):
        """Post a tweet with the given content"""
        try:
            print("Navigating to Twitter home...")
            self.driver.get("https://twitter.com/home")
            
            # Wait for and click tweet button
            print("Waiting for tweet compose box...")
            tweet_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]'))
            )
            tweet_input.send_keys(content)
            
            # Click the 'Tweet' button
            print("Clicking 'Tweet' button...")
            tweet_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweetButton"]'))
            )
            tweet_button.click()
            
            # Wait for tweet to be posted and get its URL
            print("Waiting for tweet to be posted...")
            time.sleep(3)  # Short wait for the post to process
            
            # Wait for the success indicator
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="toast"]'))
            )
            
            # Navigate to profile to get the tweet URL
            print("Getting tweet URL...")
            self.driver.get(f"https://twitter.com/{TWITTER_USERNAME}")
            time.sleep(2)  # Wait for profile to load
            
            # Get the first tweet's URL
            first_tweet = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]'))
            )
            tweet_link = first_tweet.find_element(By.CSS_SELECTOR, 'a[href*="/status/"]')
            tweet_url = tweet_link.get_attribute('href')
            
            print(f"Tweet posted successfully! URL: {tweet_url}")
            return tweet_url
            
        except Exception as e:
            print(f"Failed to post tweet: {str(e)}")
            print("Current URL:", self.driver.current_url)
            print("Page source:", self.driver.page_source[:1000])
            raise

    def close(self):
        """Close the browser"""
        if hasattr(self, 'driver'):
            self.driver.quit()

if __name__ == "__main__":
    poster = TwitterPoster()
    try:
        poster.post_tweet("Test tweet from Python! #MCP")
        input("Press Enter to close the browser...")
    finally:
        poster.close() 