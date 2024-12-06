from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import os
from config import *

class TwitterPoster:
    def __init__(self):
        try:
            os.system("taskkill /f /im chrome.exe")
            time.sleep(2)
            
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(options=options)
            self._login()
            
        except Exception as e:
            print(f"Error initializing Twitter poster: {e}")
            if hasattr(self, 'driver'):
                self.driver.quit()
            raise

    def _login(self):
        try:
            print("Logging into Twitter...")
            self.driver.get("https://twitter.com/login")
            time.sleep(3)

            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='username']"))
            )
            username_input.send_keys(TWITTER_USERNAME)
            username_input.send_keys(Keys.RETURN)
            time.sleep(2)

            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
            )
            password_input.send_keys(TWITTER_PASSWORD)
            password_input.send_keys(Keys.RETURN)
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetButtonInline']"))
            )
            print("Successfully logged into Twitter!")
            
        except Exception as e:
            print(f"Failed to login to Twitter: {e}")
            raise

    def post_tweet(self, content):
        try:
            print(f"Attempting to post tweet: {content[:50]}...")
            
            tweet_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetButtonInline']"))
            )
            tweet_button.click()
            time.sleep(2)

            tweet_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']"))
            )
            tweet_input.clear()
            tweet_input.send_keys(content)
            time.sleep(2)

            posted = False
            
            try:
                post_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='tweetButton']"))
                )
                post_button.click()
                posted = True
            except:
                print("Method 1 failed, trying method 2...")

            if not posted:
                try:
                    post_button = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='tweetButton']")
                    self.driver.execute_script("arguments[0].click();", post_button)
                    posted = True
                except:
                    print("Method 2 failed, trying method 3...")

            if not posted:
                try:
                    tweet_input.send_keys(Keys.CONTROL + Keys.RETURN)
                    posted = True
                except:
                    print("Method 3 failed...")

            if not posted:
                raise Exception("Failed to post tweet using all available methods")

            time.sleep(10)
            
            current_url = self.driver.current_url
            if "home" in current_url.lower():
                raise Exception("Tweet may not have been posted - still on home page")
            
            print(f"Successfully posted tweet! URL: {current_url}")
            return current_url

        except Exception as e:
            print(f"Failed to post tweet: {e}")
            self.driver.save_screenshot("tweet_error.png")
            print("Error screenshot saved as tweet_error.png")
            raise

    def close(self):
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Error closing browser: {e}")

    def __del__(self):
        self.close()

if __name__ == "__main__":
    poster = TwitterPoster()
    try:
        poster.post_tweet("Test tweet from Python! #MCP")
    finally:
        poster.close() 