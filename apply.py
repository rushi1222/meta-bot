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
    time.sleep(10)  # Wait before closing
    
    wait = WebDriverWait(driver, 10)
    
    # Wait for "Apply to this job" link
    apply_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div._arm- a._42ft')))
    # Scroll into view, then click
    driver.execute_script("arguments[0].scrollIntoView(true);", apply_link)
    time.sleep(3)  # <--- 3 seconds pause here
    apply_link.click()
    time.sleep(10)  # Wait for the new page to load
    
    # Close the previous tab
    driver.close()
    print("✅ only trying to close the previous tab")
    try:
        driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab if opened
        time.sleep(10)
        
        personal_page = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._9csu')))
        print("✅ Detected element with class '_9csu '")
        print("Element text content:", personal_page.text)
        
        # Check job location checkboxes (if any)
        try:
            job_locations_checkboxes = driver.find_elements(By.CSS_SELECTOR, 'div.jobLocations input._9ctg')
            for checkbox in job_locations_checkboxes:
                if not checkbox.is_selected():
                    checkbox.click()
                    print(f"✅ Checked checkbox with id: {checkbox.get_attribute('id')}")
        except Exception as e:
            print(f"✅ Failed to find or check job location checkboxes. Error: {e}")

        # Attempt to find "work_auth_question" step
        try:
            work_auth_question = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(@class, '_9ey0') and .//div[contains(@class, '_9ey1') and text()='Next']]")
                )
            )
            # Work eligibility
            try:
                work_eligible_us = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.workEligibleUS'))
                )
                yes_radio_button = work_eligible_us.find_element(
                    By.XPATH, ".//span[text()='Yes']/preceding-sibling::input[@type='radio']"
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", yes_radio_button)
                time.sleep(3)  # <--- 3 seconds pause here
                yes_radio_button.click()
                print("✅ Clicked on the 'Yes' radio button for work eligibility")
            except Exception as e:
                print(f"❌ Failed to find or click the 'Yes' radio button for work eligibility. Error: {e}")

            # Sponsorship
            try:
                requires_sponsorship = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.requiresSponsorship'))
                )
                no_radio_button = requires_sponsorship.find_element(
                    By.XPATH, ".//span[text()='No']/preceding-sibling::input[@type='radio']"
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", no_radio_button)
                time.sleep(3)  # <--- 3 seconds pause here
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

        # Next link 1
        next_link_1 = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@class, '_9ey0') and .//div[contains(@class, '_9ey1') and text()='Next']]")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", next_link_1)
        time.sleep(3)  # <--- 3 seconds pause here
        next_link_1.click()
        print("✅ Clicked on the 'next_link_1' button")

        ################Education#################
        try:
            education = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._9csu')))
            print("✅ Detected element with class '_9csu '")
            print("Element text content:", education.text)
            
            next_link_2 = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(@class, '_9ey0') and .//div[contains(@class, '_9ey1') and text()='Next']]")
                )
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", next_link_2)
            time.sleep(3)  # <--- 3 seconds pause here
            next_link_2.click()
            print("✅ Clicked on the 'next_link_2' button")
            time.sleep(3)

            #################Experience and Skills#################
            try:
                experience = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._9csu')))
                print("✅ Detected element with class '_9csu '")
                print("Element text content:", experience.text)
                
                next_link_3 = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//a[contains(@class, '_9ey0') and .//div[contains(@class, '_9ey1') and text()='Next']]")
                    )
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", next_link_3)
                time.sleep(3)  # <--- 3 seconds pause here
                next_link_3.click()
                print("✅ Clicked on the 'next_link_3' button")
                time.sleep(3)

                ###############Voluntary Self-Identification#################
                try:
                    voluntary = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._9csu')))
                    print("✅ Detected element with class '_9csu '")
                    print("Element text content:", voluntary.text)
                    
                    next_link_4 = wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//a[contains(@class, '_9ey0') and .//div[contains(@class, '_9ey1') and text()='Next']]")
                        )
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", next_link_4)
                    time.sleep(3)  # <--- 3 seconds pause here
                    next_link_4.click()
                    print("✅ Clicked on the 'next_link_4' button")
                    time.sleep(3)

                    #################Review and Submit#################
                    try:
                        submit_button = wait.until(
                            EC.element_to_be_clickable(
                                (By.CSS_SELECTOR, 'div._9eyl button')
                            )
                        )
                        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                        time.sleep(3)  # <--- 3 seconds pause here
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
                print(f"❌ Failed to open job: {job_url} at experience Error: {e}")
                return False
        except Exception as e:
            print(f"❌ Failed to open job: {job_url} at education Error: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Failed to open job: {job_url} at personal info. Error: {e}")
        return False


def open_job_link(driver, job_url):
    """
    Opens a job link in a new tab, waits, then closes the tab.
    """
    return apply(driver, job_url)
