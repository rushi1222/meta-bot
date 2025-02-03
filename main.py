import yaml
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from apply import open_job_link  # Import function
from email_notifier import send_email  # Import email function

# Load credentials and job links from config.yaml
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

EMAIL = config["meta_login"]["email"]
PASSWORD = config["meta_login"]["password"]
JOB_LINKS = config["job_links"]

# Set up Selenium WebDriver
options = Options()
options.add_argument("--start-maximized")  # Open browser in full-screen mode
options.add_argument("--disable-blink-features=AutomationControlled")  # Reduce bot detection
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds for elements to load

# Open Meta Careers Login Page
driver.get("https://www.metacareers.com/login")
print("✅ Opened Meta Careers login page.")
time.sleep(2)  # Give the page a moment to start rendering

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

    # (Optional) Give time for login to process
    time.sleep(5)
    print("✅ Login successful. Now opening job links.")

    # Loop through job links and apply
    for job_url in JOB_LINKS:
        try:
            result = open_job_link(driver, job_url)  # Open job link
            if result:
                subject = "✅ Meta Application Successful"
                body = f"Your job application for {job_url} was successfully submitted."
                print(f"✅ Successfully applied to job: {job_url}")
            else:
                subject = "❌ Meta Application Failed"
                body = f"Your job application for {job_url} failed."
                print(f"❌ Failed to apply to job: {job_url}")

            # Send email notification
            send_email(subject, body)
        except Exception as e:
            print(f"❌ Failed to open job: {job_url}. Error: {e}")  # Log error

        time.sleep(20)  # Small delay before next job
    
    print("🎉 All jobs applied to. Closing browser."
          )
    driver.quit()  # Close the browser
except Exception as e:
    print(f"❌ Error during login or main process: {e}")
    driver.quit()

# Keep the browser open indefinitely
while True:
    time.sleep(1)
