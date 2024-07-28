
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By



def read_file(file_path):
    """Read content from a file."""
    with open(file_path, 'r') as file:
        return file.read().strip()
# Read proxies from file



extention_path  = 'J2TEAM-Cookies-Chrome-Web-Store.crx'

chromedriver_path = 'chromedriver.exe'

chrome_options = Options()

chrome_options.add_argument(f"webdriver.chrome.driver= {ChromeDriverManager().install()}")
chrome_options.add_extension(extention_path)

driver = webdriver.Chrome(options=chrome_options)

time.sleep(5)



driver.get("https://www.tiktok.com")






driver.get("chrome-extension://okpidcojinmlaakglciglbpcpajaibco/popup.html")
driver.find_element(By.XPATH, "/html/body/div/main/div/div[1]/div[2]/div[3]/div[2]/div/div/button").click()
time.sleep(0.8)
driver.find_element(By.XPATH, "/html/body/div/main/div/div[1]/div[2]/div[3]/div[2]/div[2]/div[2]").click()
cookies = read_file('cookies/1.txt')
input_element = driver.find_element(By.XPATH, "/html/body/div/main/div/div[3]/div/div[2]/textarea")
# Use JavaScript to simulate pasting the content into the input field
script = """
var input = arguments[0];
var text = arguments[1];
input.focus();
input.value = text;
var event = new Event('input', { bubbles: true });
input.dispatchEvent(event);
"""
driver.execute_script(script, input_element, cookies)
time.sleep(0.8)
import_button = driver.find_element(By.XPATH, "/html/body/div/main/div/div[3]/div/div[3]/div/div")
import_button.click()
time.sleep(2)
driver.switch_to.window(driver.window_handles[0])

driver.get("https://www.tiktok.com/business-suite/business-registration/verifyAccess")
    
time.sleep(50)
driver.quit()