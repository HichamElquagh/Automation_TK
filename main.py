# hicham code
import logging
import time
import threading
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Configure logging
logging.basicConfig(level=logging.DEBUG)
extention_path  = 'J2TEAM-Cookies-Chrome-Web-Store.crx'

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
         
     
# Select a proxy randomly
proxy = proxies[0].strip()

# Extract proxy details
proxy_parts = proxy.split(':')
if len(proxy_parts) == 4:
    proxy_host, proxy_port, proxy_user, proxy_pass = proxy_parts
else:
    logging.error("Proxy format is incorrect. Expected format: host:port:user:pass")
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


def open_browser_instance(instance_id):
    # Initialize the Chrome driver with service, selenium-wire options, and chrome options
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        seleniumwire_options=seleniumwire_options,
        options=options,

    )
    
    # Navigate to the target webpage
    try:
        time.sleep(10)
        set_cookies_extentions(driver)
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
for i in range(4):
    thread = threading.Thread(target=open_browser_instance, args=(i+1,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

# hicham code

