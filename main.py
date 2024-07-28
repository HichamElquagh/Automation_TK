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

# Read proxies from file
proxy_file_path = 'proxy/PROXY.txt'
with open(proxy_file_path, 'r') as file:
    proxies = file.readlines()

# Select the first proxy from the list
if proxies:
    for proxy in proxies:
        proxy = proxy.strip()
        if proxy:
            break   
    logging.info(f"Selected proxy: {proxy}") 
else:
    logging.error("No proxies found in the file.")
    raise Exception("No proxies found in the file.")

# Extract proxy details
proxy_parts = proxy.split(':')
if len(proxy_parts) == 4:
    proxy_host, proxy_port, proxy_user, proxy_pass = proxy_parts
else:
    logging.error("Proxy format is incorrect. Expected format: host:port:user:pass")
    raise Exception("Proxy format is incorrect. Expected format: host:port:user:pass")

# Construct the proxy URL
proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
logging.debug(f"Proxy URL: {proxy_url}")

# Set selenium-wire options to use the proxy
seleniumwire_options = {
    "proxy": {
        "http": proxy_url,
        "https": proxy_url
    },
}

# Set Chrome options to run in headless mode
options = Options()
# options.add_argument("--headless=new")

def open_browser_instance(instance_id):
    # Initialize the Chrome driver with service, selenium-wire options, and chrome options
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        seleniumwire_options=seleniumwire_options,
        options=options
    )
    
    # Navigate to the target webpage
    try:
        driver.get("https://tiktok.com")
        time.sleep(50)
        logging.info(f"Browser instance {instance_id} successfully navigated to https://tiktok.com")
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

