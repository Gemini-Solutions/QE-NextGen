from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def successful_login_with_valid_credentials():
    try:
        driver = webdriver.Firefox()
        driver.get("your_login_page_url")

        # Wait for the page and content to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Enter user name"]')))

        # Input valid credentials
        username_input = driver.find_element(By.XPATH, '//*[@id="Enter user name"]')
        password_input = driver.find_element(By.XPATH, '//*[@id="passwd"]')
        pin_token_input = driver.find_element(By.XPATH, '//*[@id="passwd1"]')

        username_input.send_keys("valid_username")
        password_input.send_keys("valid_password")
        pin_token_input.send_keys("valid_pin_token")

        # Click on the 'Log On' button
        logon_button = driver.find_element(By.XPATH, '//*[@id="Log_On"]')
        logon_button.click()

        # Wait for redirection to remote resources page
        WebDriverWait(driver, 10).until(EC.url_contains("remote_resources"))

    except Exception as e:
        print(f"Error: {e}")

    finally:
        time.sleep(2)
        driver.quit()

def unsuccessful_login_with_invalid_credentials():
    try:
        driver = webdriver.Firefox()
        driver.get("https://remote.pimco.com/vpn/index.html")

        # Wait for the page and content to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Enter user name"]')))

        # Input invalid credentials
        username_input = driver.find_element(By.XPATH, '//*[@id="Enter user name"]')
        password_input = driver.find_element(By.XPATH, '//*[@id="passwd"]')
        pin_token_input = driver.find_element(By.XPATH, '//*[@id="passwd1"]')

        username_input.send_keys("invalid_username")
        password_input.send_keys("invalid_password")
        pin_token_input.send_keys("invalid_pin_token")

        # Click on the 'Log On' button
        logon_button = driver.find_element(By.XPATH, '//*[@id="Log_On"]')
        logon_button.click()

        # Wait for error message to be displayed
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"invalid credentials")]')))

    except Exception as e:
        print(f"Error: {e}")

    finally:
        time.sleep(2)
        driver.quit()

def forgot_password_recovery():
    try:
        driver = webdriver.Firefox()
        driver.get("your_login_page_url")

        # Wait for the page and content to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Forgot_Password_Link"]')))

        # Click on the 'Forgot Password' link
        forgot_password_link = driver.find_element(By.XPATH, '//*[@id="Forgot_Password_Link"]')
        forgot_password_link.click()

        # Wait for the password recovery page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Email_Input"]')))

        # Enter registered email address for password recovery
        email_input = driver.find_element(By.XPATH, '//*[@id="Email_Input"]')
        email_input.send_keys("registered_email@example.com")

        # Complete the necessary verification steps

        # After verification, wait for the email with instructions
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"Password reset instructions sent")]')))

    except Exception as e:
        print(f"Error: {e}")

    finally:
        time.sleep(2)
        driver.quit()

def account_lockout_after_multiple_failed_login_attempts():
    try:
        driver = webdriver.Chrome()
        driver.get("your_login_page_url")

        # Wait for the page and content to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Enter user name"]')))

        for _ in range(5):  # Simulate multiple failed login attempts
            # Input incorrect credentials
            username_input = driver.find_element(By.XPATH, '//*[@id="Enter user name"]')
            password_input = driver.find_element(By.XPATH, '//*[@id="passwd"]')
            pin_token_input = driver.find_element(By.XPATH, '//*[@id="passwd1"]')

            username_input.send_keys("incorrect_username")
            password_input.send_keys("incorrect_password")
            pin_token_input.send_keys("incorrect_pin_token")

            # Click on the 'Log On' button
            logon_button = driver.find_element(By.XPATH, '//*[@id="Log_On"]')
            logon_button.click()

            # Wait for error message to be displayed
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"invalid credentials")]')))

        # After multiple failed attempts, wait for account lockout notification
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"Account locked out")]')))

    except Exception as e:
        print(f"Error: {e}")

    finally:
        time.sleep(2)
        driver.quit()

# Call the functions
# successful_login_with_valid_credentials()
unsuccessful_login_with_invalid_credentials()
# forgot_password_recovery()
# account_lockout_after_multiple_failed_login_attempts()
