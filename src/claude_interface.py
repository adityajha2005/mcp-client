from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import time

CLAUDE_DESKTOP_URL = "https://claude.ai"
USER_DATA_DIR = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data'
FREE_PLAN_MESSAGE_LIMIT = 4000  # Characters

class ClaudeInterface:
    def __init__(self):
        try:
            # Kill any existing Chrome processes before starting
            os.system("taskkill /f /im chrome.exe")
            time.sleep(2)  # Wait for processes to be killed
            
            options = webdriver.ChromeOptions()
            options.add_argument(f"user-data-dir={USER_DATA_DIR}")
            options.add_argument("profile-directory=Default")
            
            # Browser stability options
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-first-run")
            options.add_argument("--no-service-autorun")
            options.add_argument("--password-store=basic")
            
            # Browser settings
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            print("Launching browser with your profile...")
            service = webdriver.ChromeService()
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Wait for browser initialization
            print("Waiting for browser to initialize...")
            time.sleep(3)
            
            # Remove webdriver flag
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("Navigating to Claude.ai...")
            self.driver.get(CLAUDE_DESKTOP_URL)
            
            print("Waiting for chat interface to load...")
            try:
                print("This may take up to 2 minutes. Press Ctrl+C to cancel...")
                
                # Wait for page load
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                # Check for service errors
                self._check_for_errors()
                
                # Wait for chat interface
                print("Waiting for Claude's chat interface...")
                WebDriverWait(self.driver, 120).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".prose"))
                )
                
                # Check plan status
                self._check_plan_status()
                
                # Wait for input field
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[placeholder*='Message']"))
                )
                print("Successfully loaded Claude.ai chat interface!")
                
            except Exception as e:
                print(f"Failed to load Claude.ai interface: {e}")
                print(f"Current URL: {self.driver.current_url}")
                raise
                
        except KeyboardInterrupt:
            print("\nStartup cancelled by user. Cleaning up...")
            if hasattr(self, 'driver'):
                self.driver.quit()
            raise SystemExit(1)
        except Exception as e:
            print(f"An error occurred during initialization: {e}")
            if hasattr(self, 'driver'):
                self.driver.quit()
            raise

    def _check_for_errors(self):
        """Check for any error messages on the page"""
        try:
            error_message = self.driver.find_element(By.XPATH, "//*[contains(text(), 'unable to serve your request')]")
            if error_message:
                print("Service error detected. Refreshing page...")
                self.driver.refresh()
                time.sleep(5)  # Wait for refresh
                # Check again after refresh
                error_message = self.driver.find_element(By.XPATH, "//*[contains(text(), 'unable to serve your request')]")
                if error_message:
                    raise Exception("Claude.ai service is currently unavailable")
        except NoSuchElementException:
            pass  # No error message found
        except Exception as e:
            if "no such element" not in str(e).lower():  # Ignore if error message not found
                raise

    def _check_plan_status(self):
        """Check if we're on free plan and handle limitations"""
        try:
            plan_element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Using limited free plan')]")
            if plan_element:
                print("WARNING: Running on limited free plan. Some features may be restricted.")
                self.is_free_plan = True
                # Get remaining messages if possible
                try:
                    limit_text = self.driver.find_element(By.XPATH, "//*[contains(@class, 'remaining-messages')]").text
                    print(f"Plan status: {limit_text}")
                except NoSuchElementException:
                    pass
        except NoSuchElementException:
            self.is_free_plan = False

    def _wait_for_response(self, timeout=120):
        """Wait for and return Claude's response"""
        start_time = time.time()
        last_response_text = None
        
        while time.time() - start_time < timeout:
            try:
                # Check for errors while waiting
                self._check_for_errors()
                
                # Look for response elements
                responses = self.driver.find_elements(By.CSS_SELECTOR, ".prose")
                if responses:
                    current_response = responses[-1].text
                    
                    # If response hasn't changed in 5 seconds, consider it complete
                    if current_response == last_response_text:
                        if time.time() - last_response_time > 5:
                            return current_response
                    else:
                        last_response_text = current_response
                        last_response_time = time.time()
                
                time.sleep(1)
                
            except Exception as e:
                if "unable to serve your request" in str(e).lower():
                    raise
                print(f"Warning: Error while waiting for response: {e}")
        
        raise TimeoutException("No response received from Claude within timeout period")

    def send_message(self, message):
        """Send a message to Claude and return its response"""
        try:
            # Check for errors before sending
            self._check_for_errors()
            
            if hasattr(self, 'is_free_plan') and self.is_free_plan:
                if len(message) > FREE_PLAN_MESSAGE_LIMIT:
                    raise ValueError(f"Message exceeds free plan length limit of {FREE_PLAN_MESSAGE_LIMIT} characters")

            # Find and interact with input field
            input_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[placeholder*='Message']"))
            )
            
            # Clear any existing text
            input_field.clear()
            
            # Send message in chunks to avoid any potential issues with long messages
            chunk_size = 1000
            for i in range(0, len(message), chunk_size):
                chunk = message[i:i + chunk_size]
                input_field.send_keys(chunk)
                time.sleep(0.1)  # Small delay between chunks
            
            # Send message
            input_field.send_keys(Keys.RETURN)
            
            # Wait for and return response
            return self._wait_for_response()
            
        except Exception as e:
            error_msg = str(e)
            if "exceeds free plan" in error_msg:
                print("Consider upgrading your Claude plan for longer messages")
            elif "service is currently unavailable" in error_msg:
                print("Claude service is experiencing issues. Try again later")
            elif "timeout" in error_msg.lower():
                print("Claude took too long to respond. The message might be too complex.")
            raise

    def close(self):
        """Properly close the browser"""
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Error while closing browser: {e}")

    def __del__(self):
        """Destructor to ensure browser is closed"""
        self.close() 