import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def apply(driver, job_url):
    """
    Opens a job link in a new tab, waits, then closes the tab.
    """
    print(f"🌐 Opening job link: {job_url}")
    
    # Open new tab
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])  # Switch to new tab
    
    # Load the job page
    driver.get(job_url)
    time.sleep(5)  # Wait before closing
    wait = WebDriverWait(driver, 10)
    # Wait for "Apply to this job" link
    apply_link = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div._arm- a._42ft'))
    )
    apply_link.click()
    time.sleep(3)  # Wait for the new page to load
    # Close the previous tab
    driver.close()
    print("✅ only trying to close the previous tab")
    try:
        driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab if opened
        time.sleep(10)
        personal_page = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div._9csu'))
        )
        print("✅ Detected element with class '_9csu '")
        print("Element text content:", personal_page.text)
        # find if this class _9ctg is present if present there can be multiple input type checkbox check them all if not its fine just keep going
        try:
            job_locations_checkboxes = driver.find_elements(By.CSS_SELECTOR, 'div.jobLocations input._9ctg')
            for checkbox in job_locations_checkboxes:
                if not checkbox.is_selected():
                    checkbox.click()
                    print(f"✅ Checked checkbox with id: {checkbox.get_attribute('id')}")
        except Exception as e:
            print(f"✅ Failed to find or check job location checkboxes. Error: {e}")

        # find if this class _9ct7 is present or not if present then click on it or else just just print not found and keep going
        try:
            work_auth_question = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(@class, '_9ey0') and .//div[contains(@class, '_9ey1') and text()='Next']]")
                )
            )
            # if found then search for class containing workEligibleUS and in its children div find radio button Yes and click on it
            try:
                work_eligible_us = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.workEligibleUS'))
                )
                yes_radio_button = work_eligible_us.find_element(By.XPATH, ".//span[text()='Yes']/preceding-sibling::input[@type='radio']")
                yes_radio_button.click()
                print("✅ Clicked on the 'Yes' radio button for work eligibility")
            except Exception as e:
                print(f"❌ Failed to find or click the 'Yes' radio button for work eligibility. Error: {e}")

            try:
                #requiresSponsorship
                requires_sponsorship = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.requiresSponsorship'))
                )
                no_radio_button = requires_sponsorship.find_element(By.XPATH, ".//span[text()='No']/preceding-sibling::input[@type='radio']")
                no_radio_button.click()
                print("✅ Clicked on the 'No' radio button for requires sponsorship")
            except Exception as e:
                print(f"❌ Failed to find or click the 'No' radio button for requires sponsorship. Error: {e}")
            time.sleep(3)
            print("✅'work_auth_question found'")
            time.sleep(3)
        except Exception as e:
            print(f" ✅ not found _9ct7 continue to next page")

            time.sleep(3)
        next_link_1 = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@class, '_9ey0') and .//div[contains(@class, '_9ey1') and text()='Next']]")
            )
        )
        next_link_1.click()
        print("✅ Clicked on the 'next_link_1' button")

        ################Education#################

        try:
            education = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div._9csu'))
            )
            print("✅ Detected element with class '_9csu '")
            print("Element text content:", education.text)
            next_link_2 = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(@class, '_9ey0') and .//div[contains(@class, '_9ey1') and text()='Next']]")
                )
            )
            next_link_2.click()
            print("✅ Clicked on the 'next_link_2' button")
            time.sleep(3)

            #################Experience and Skills#################

            try:
                experience = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div._9csu'))
                )
                print("✅ Detected element with class '_9csu '")
                print("Element text content:", experience.text)
                next_link_3 = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//a[contains(@class, '_9ey0') and .//div[contains(@class, '_9ey1') and text()='Next']]")
                    )
                )
                next_link_3.click()
                print("✅ Clicked on the 'next_link_3' button")
                time.sleep(3)

                ###############Voluntary Self-Identification#################

                try:
                    voluntary = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div._9csu'))
                    )
                    print("✅ Detected element with class '_9csu '")
                    print("Element text content:", voluntary.text)
                    next_link_4 = wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//a[contains(@class, '_9ey0') and .//div[contains(@class, '_9ey1') and text()='Next']]")
                        )
                    )
                    next_link_4.click()
                    print("✅ Clicked on the 'next_link_4' button")
                    time.sleep(3)

                    #################Review and Submit#################
                    try:
                        # find button element under the parent class _9eyl
                        submit_button = wait.until(
                            EC.element_to_be_clickable(
                                (By.CSS_SELECTOR, 'div._9eyl button')
                            )
                        )
                        submit_button.click()
                        print("✅ Clicked on the 'submit' button")
                        time.sleep(10)
                        # Close the current tab
                        driver.close()
                        print("✅ Closed the current tab")
                        # Switch back to the main window
                        driver.switch_to.window(driver.window_handles[0])
                        return True

                    except Exception as e:
                        print(f"❌ Failed to open job: {job_url} at review and submit Error: {e}")
                        return False
                except Exception as e:
                    print(f"❌ Failed to open job: {job_url} at voluntary Error: {e}")
                    return False

            except Exception as e:
                print(f"❌ Failed to open job: {job_url} at experience Error: {e}")  # Log error
                return False

        except Exception as e:
            print(f"❌ Failed to open job: {job_url} at education Error: {e}")  # Log error
            return False
        
    except Exception as e:
        print(f"❌ Failed to open job: {job_url} at personal info. Error: {e}")  # Log error
        return False
    # ...here you can add more complex logic...

def open_job_link(driver, job_url):
    """
    Opens a job link in a new tab, waits, then closes the tab.
    """
    return apply(driver, job_url)

    # driver.close()
    # driver.switch_to.window(driver.window_handles[0])
    # print("✅ Job tab closed. Moving to next job...")

