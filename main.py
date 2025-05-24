import os
import time
import yaml
from dotenv import load_dotenv

from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from apply import open_job_link
from email_notifier import send_email

# ✅ Load environment variables
load_dotenv()

# ✅ Credentials from .env
EMAIL = os.getenv("META_EMAIL")
PASSWORD = os.getenv("META_PASSWORD")

# ✅ Load job links from config.yaml
with open("config.yaml", "r") as file:
    JOB_LINKS = yaml.safe_load(file)["job_links"]

# ✅ Configure ChromeOptions for local execution
options = Options()
# Uncomment this for headless mode:
# options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

# ✅ Selenium Wire options
seleniumwire_options = {
    "verify_ssl": True,
    "request_storage": "memory",
    "disable_capture": True
}

# ✅ Use ChromeDriverManager for local Chrome
print("🔹 Using ChromeDriverManager for local Chrome.")
driver_path = ChromeDriverManager().install()

# ✅ Build WebDriver
driver = webdriver.Chrome(
    service=Service(driver_path),
    options=options,
    seleniumwire_options=seleniumwire_options
)

# ✅ Intercept requests (spoof headers)
def interceptor(request):
    request.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    })
driver.request_interceptor = interceptor

wait = WebDriverWait(driver, 10)

# ✅ Open Meta Careers
driver.get("https://www.metacareers.com/login")
print("✅ Opened Meta Careers login page.")
time.sleep(2)

try:
    # Login steps
    email_field = wait.until(EC.presence_of_element_located((By.ID, "js_1")))
    email_field.send_keys(EMAIL)
    print("✅ Entered Email")

    password_field = wait.until(EC.presence_of_element_located((By.ID, "js_b")))
    password_field.send_keys(PASSWORD)
    print("✅ Entered Password")

    password_field.send_keys(Keys.RETURN)
    print("➡️ Pressed ENTER to log in.")

    time.sleep(5)
    print("✅ Login successful. Now opening job links.")

    for job_url in JOB_LINKS:
        try:
            result = open_job_link(driver, job_url)
            if result:
                subject = "✅ Meta Application Successful"
                body = f"Your job application for {job_url} was successfully submitted."
                print(f"✅ Successfully applied to job: {job_url}")
            else:
                subject = "❌ Meta Application Failed"
                body = f"Your job application for {job_url} failed."
                print(f"❌ Failed to apply to job: {job_url}")

            send_email(subject, body)

        except Exception as e:
            print(f"❌ Failed to open job: {job_url}. Error: {e}")

        time.sleep(20)

    print("🎉 All jobs applied to. Closing browser.")

except Exception as e:
    print(f"❌ Error during login or main process: {e}")

finally:
    driver.quit()
    print("✅ Script completed. Exiting.")
