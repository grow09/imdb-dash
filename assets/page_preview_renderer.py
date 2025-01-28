from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Process
import time
import os

def capture_screenshot(url, output_path):

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920x1080')
    options.add_argument('--zoom=0.5')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(15)
    # Trigger the callbacks by scrolling the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, 0);")

    try:
        # Explicit wait for an element to ensure the page is loaded
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    except Exception as e:
        print(f"Error loading page {url}: {e}")
    else:
        driver.save_screenshot(output_path)

    driver.quit()


if __name__ == "__main__":
    pages_dir = 'pages'
    pages = [name for name in os.listdir(pages_dir) if os.path.isdir(os.path.join(pages_dir, name)) and name != 'home']

    base_url = "http://127.0.0.1:8050"

    urls_and_paths = [(f"{base_url}/{name}/", f"assets/{name}_preview.png") for name in pages]

    processes = []
    for url, path in urls_and_paths:
        process = Process(target=capture_screenshot, args=(url, path))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()
    
    end_time = time.time()


## test line