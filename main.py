# hicham code
import logging
import time
import threading
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# from selenium.webdriver.common.keys import Keys

# Configure logging
# logging.basicConfig(level=logging.DEBUG)
extention_path  = 'J2TEAM-Cookies-Chrome-Web-Store.crx'
clear_data_browser_extention_path = 'Clear-Browsing-Data-Chrome-Web-Store.crx'
NUMBERS_FILE_PATH = r'C:\Users\alqua\Desktop\Automation_TK\numbers\1721733173254.txt'

# Coordinates for the area to capture (top-left and bottom-right)
TOP_LEFT_X = 183
TOP_LEFT_Y = 188
BOTTOM_RIGHT_X = 319
BOTTOM_RIGHT_Y = 273

# Calculate width and height from the specified coordinates
WIDTH = BOTTOM_RIGHT_X - TOP_LEFT_X
HEIGHT = BOTTOM_RIGHT_Y - TOP_LEFT_Y
def click_on_coordinates(coordinates):
    """Click on the coordinates using pyautogui."""
    for x, y in coordinates:
        print(f"Clicking on coordinates: ({x}, {y})")
        pyautogui.click(x, y)
        time.sleep(1)
def solve_captcha(driver):
    """Handle CAPTCHA solving loop."""
    while True:
        try:
            captcha_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, 'captcha-verify-image'))
            )
            print("Captcha found, wait for solving.")
            time.sleep(5)
            region = (TOP_LEFT_X, TOP_LEFT_Y, WIDTH, HEIGHT)
            screenshot_path = r'C:\Users\Maria1\Desktop\Auto-caller-project-Selenium-wire\Captcha-Screenshots'
            timestamp = int(time.time())
            screenshot_path = os.path.join(screenshot_path, f"screenshot_{timestamp}.png")
            take_screenshot(screenshot_path, region)
            result_url = post_screenshot(API_URL, API_KEY, screenshot_path)
            if result_url:
                print(f"Captcha solving URL: {result_url}")
                time.sleep(1)
                response = requests.get(result_url)
                if response.status_code == 200:
                    print(f"API response: {response.text}")
                    coordinates = parse_coordinates(response.text)
                    if coordinates:
                        click_on_coordinates(coordinates)
                        print(f"Clicked on coordinates: {coordinates}")
                        time.sleep(2)
                        confirm_button = driver.find_element(By.XPATH, '//*[@id="captcha_container"]/div/div[3]/div[2]')
                        confirm_button.click()
                        print("Confirm button clicked.")
                        time.sleep(2)
                        WebDriverWait(driver, 5).until_not(
                            EC.presence_of_element_located((By.CLASS_NAME, 'captcha-disable-scroll'))
                        )
                        print("Captcha solved successfully.")
                        return True
                    else:
                        print("Failed to solve captcha.")
            else:
                print("Failed to solve captcha.")
        except TimeoutException:
            print("Captcha not found initially. Retrying...")
            refresh_button = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/div[1]/a[1]/span[2]')
            refresh_button.click()
            print("Refresh button clicked.")
            time.sleep(5)
            continue
        return False


def read_file(file_path):
    """Read content from a file."""
    with open(file_path, 'r') as file:
        return file.read().strip()
# Read proxies from file
proxy_file_path = 'proxy/PROXY.txt'
with open(proxy_file_path, 'r') as file:
    proxies = file.readlines()

def set_cookies_extentions (driver):
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


def clear_data_browser(driver):
     # Locate and click Clear data extension button 
        driver.get("chrome-extension://bjilljlpencdcpihofiobpnfgcakfdbe/src/action/index.html")
        time.sleep(1)
        clear_data = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[1]/div[2]/div")
        clear_data.click()
        time.sleep(3)    
def get_first_number(file_path):
    """Read the first number from the file and remove it."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    if not lines:
        return None
    first_number = lines[0].strip()
    with open(file_path, 'w') as file:
        file.writelines(lines[1:])
    return first_number     
# Select a proxy randomly
proxy = proxies[0].strip()

# Extract proxy details
proxy_parts = proxy.split(':')
if len(proxy_parts) == 4:
    proxy_host, proxy_port, proxy_user, proxy_pass = proxy_parts
else:
    # logging.error("Proxy format is incorrect. Expected format: host:port:user:pass")
    raise Exception("Proxy format is incorrect. Expected format: host:port:user:pass")


# Set selenium-wire options to use the proxy
seleniumwire_options = {
    "proxy": {
        "http":  f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}",
        "https":  f"https://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}",
        'no_proxy': 'localhost,127.0.0.1'  # Bypass proxy for localhost

    },
}

# Set Chrome options to run in headless mode
options = Options()
options.add_extension(extention_path)
options.add_extension(clear_data_browser_extention_path) 



def open_browser_instance(instance_id):
    chrome_driver_path = ChromeDriverManager().install()
    service = Service(chrome_driver_path)



    # Initialize the Chrome driver with service, selenium-wire options, and chrome options
    driver = webdriver.Chrome(
        service=service,
        seleniumwire_options=seleniumwire_options,
        options=options,

    )

    driver.maximize_window()

    
    # Navigate to the target webpage
    try:

        clear_data_browser(driver)
        time.sleep(10)
        set_cookies_extentions(driver)
        time.sleep(5)
        phone_number = get_first_number(NUMBERS_FILE_PATH)
        if phone_number:
            find_radio =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[1]/div[2]/label[1]/div')))
            find_radio.click()
            time.sleep(5)
            phone_input = driver.find_element(By.CLASS_NAME, 'phone-input')
            phone_input.clear()
            phone_input.send_keys(phone_number)
            driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[1]/div[2]/div[2]/div[2]/button').click()
            print(f"Sent phone number: {phone_number}")
            
            time.sleep(2)                    
        else:
            print("No numbers in txt file")
        time.sleep(50)

    except Exception as e:
        logging.error(f"Error navigating to https://tiktok.com in browser instance {instance_id}: {e}")
    finally:
        # Close the driver
        driver.quit()
        logging.info(f"Browser instance {instance_id} closed.")

# List to store threads
threads = []

# Create and start 4 threads for browser instances
for i in range(1):
    thread = threading.Thread(target=open_browser_instance, args=(i+1,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

# hicham code

