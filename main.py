import os
import time
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from apply import open_job_link
from email_notifier import send_email

# Load credentials from environment variables
EMAIL = os.getenv("META_EMAIL")
PASSWORD = os.getenv("META_PASSWORD")
JOB_LINKS = os.getenv("META_JOB_LINKS", "").split(",")  # Store job links as comma-separated env variable

# Set up Selenium WebDriver with headless mode for GitHub Actions
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

# Open Meta Careers Login Page
driver.get("https://www.metacareers.com/login")
print("✅ Opened Meta Careers login page.")
time.sleep(2)

try:
    # Locate and fill in Email
    email_field = wait.until(EC.presence_of_element_located((By.ID, "js_1")))
    email_field.send_keys(EMAIL)
    print("✅ Entered Email")

    # Locate and fill in Password
    password_field = wait.until(EC.presence_of_element_located((By.ID, "js_b")))
    password_field.send_keys(PASSWORD)
    print("✅ Entered Password")

    # Press ENTER to submit
    password_field.send_keys(Keys.RETURN)
    print("➡️ Pressed ENTER to log in.")

    time.sleep(5)  # Wait for login to process
    print("✅ Login successful. Now opening job links.")

    # Loop through job links and apply
    for job_url in JOB_LINKS:
        try:
            result = open_job_link(driver, job_url)
            subject = "✅ Meta Application Successful" if result else "❌ Meta Application Failed"
            body = f"Your job application for {job_url} was {'successfully submitted' if result else 'unsuccessful'}."
            print(f"{subject} for job: {job_url}")
            send_email(subject, body)
        except Exception as e:
            print(f"❌ Failed to open job: {job_url}. Error: {e}")
        time.sleep(20)

    print("🎉 All jobs applied to. Closing browser.")
    driver.quit()
except Exception as e:
    print(f"❌ Error during login or main process: {e}")
    driver.quit()
