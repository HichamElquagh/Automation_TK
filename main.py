from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os
import json


# Set the path to the J2TEAM extension
extension_path = 'J2TEAM-Cookies-Chrome-Web-Store.crx'

# Set the path to the cookies directory
cookies_directory = 'cookies'

# Set the phone numbers to import
phone_numbers = ['1234567890', '9876543210']

# Set the path to the ChromeDriver executable
chromedriver_path = 'chromedriver.exe'

# Set the path to the ChromeDriver executable in ChromeOptions
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without opening a browser window)
chrome_options.add_argument(f"webdriver.chrome.driver={chromedriver_path}")
chrome_options.add_extension(extension_path)


# Initialize Chrome WebDriver with the specified options
driver = webdriver.Chrome(options=chrome_options)

# Navigate to a URL (example: Google)
driver.get('https://www.google.com')

time.sleep(5)
# Clear all cookies
driver.delete_all_cookies()

# Load the TikTok login page
driver.get('https://www.tiktok.com/login')



# Import cookies from the cookies directory
for cookie_file in os.listdir(cookies_directory):
    with open(os.path.join(cookies_directory, cookie_file), 'r') as f:
        cookie_data = json.load(f)
        driver.add_cookie(cookie_data)

# # Refresh the page to apply the imported cookies
# driver.refresh()

# Handle the phone number input
phone_input = driver.find_element_by_id('phone-input')
for phone_number in phone_numbers:
    phone_input.send_keys(phone_number)
    # Handle any other necessary steps here, such as clicking a button to submit the phone number

# Close the browser
driver.quit()