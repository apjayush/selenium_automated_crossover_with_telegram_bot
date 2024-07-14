import schedule
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import pyotp
import json
import telebot
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

username = os.getenv('USER_NAME')
password = os.getenv('PASS_WORD')
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')
totp_secret = os.getenv('TOKEN')  # Replace with your actual TOTP secret key

def run_script():
    # Path to your ChromeDriver


    # Initialize the Chrome driver
    try:
        driver = webdriver.Chrome()
    except WebDriverException as e:
        print(f"Failed to initialize ChromeDriver: {e}")
        return

    # Open the desired website
    driver.get("https://www.streak.tech/login")

    try:
        # Adjust the timeout value and the element you are waiting for as needed
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'jss161') and contains(@class, 'jss167')]//p[text()='Log in with Kite']"))
        )
        print("Button found, clicking on it...")
        button.click()

        # Simulate entering User ID and Password
        user_id_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "userid"))  # Replace with actual User ID input field ID
        )
        user_id_input.clear()
        user_id_input.send_keys(username)  # Replace with your actual User ID

        time.sleep(1)

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))  # Replace with actual Password input field ID
        )
        password_input.clear()
        password_input.send_keys(password)  # Replace with your actual Password

        time.sleep(1)

        # Example: Click the login button after entering credentials
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        login_button.click()

        time.sleep(1)

        # Wait for the TOTP input field
        totp_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='••••••']"))  # Adjust XPath to target the TOTP input field
        )

        # Generate TOTP code if needed
        totp = pyotp.TOTP(totp_secret)
        totp_code = totp.now()

        time.sleep(1)
        # Enter TOTP code into the input field
        totp_input.clear()
        totp_input.send_keys(totp_code)

        time.sleep(2)

        # Example: Click the submit button after entering TOTP (if applicable)
        submit_button_after_totp = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]"))
        )
        submit_button_after_totp.click()
        time.sleep(2)

    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        # Navigate directly to the scanners page URL
        scanners_url = "https://www.streak.tech/scanner/movingaveragescanner"
        driver.get(scanners_url)

        print("Navigated to Scanners page successfully!")

        time.sleep(2)

    except Exception as e:
        print(f"An error occurred: {e}")  

    try:
        # Adjust the timeout value and the element you are waiting for as needed
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Run & Save Scan')]"))
        )
        print("Button found, clicking on it...")
        button.click()

        time.sleep(5)

        try:
            # Find the tbody element
            tbody_element = driver.find_element(By.CSS_SELECTOR, 'tbody[role="rowgroup"]')

            # Find all tr elements within the tbody
            all_rows = tbody_element.find_elements(By.TAG_NAME, 'tr')

            desired_texts = []
            for row in all_rows:
                # Find the p element within the current row
                p_element = row.find_element(By.TAG_NAME, 'p')
                desired_text = p_element.text
                desired_texts.append(desired_text)

            with open('best_results.json', 'r') as f:
                data = json.load(f)

            my_stocks = list(set(desired_texts) & set(data))

            print(my_stocks)

            # Send message through telegram
            bot = telebot.TeleBot(bot_token)

            for item in my_stocks:
                bot.send_message(chat_id, item)

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    except Exception as e:
        print(f"An error occurred: {e}")

    time.sleep(5)

    # Print the title of the webpage
    print(driver.title)

    # Close the browser
    driver.quit()

run_script()