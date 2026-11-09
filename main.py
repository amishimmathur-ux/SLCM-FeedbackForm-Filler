
from selenium import webdriver
from feedback_bot import fill_feedback_form, debug_controls
import json
import time

URL = "https://mujslcm.jaipur.manipal.edu/Student"


def main():

    # Load configuration
    with open("config.json", "r") as file:
        config = json.load(file)

    answer = config.get("default_answer", "Yes")

    # Open Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    try:

        # Open MUJ portal
        driver.get(URL)

        print("MUJ Feedback Bot Started!")

        input("\nLog in and open a pending feedback form.")
        input("Press ENTER when the questionnaire is open...")

        time.sleep(2)

        # Inspect controls first
        print("\n========== CONTROL INSPECTION ==========")
        debug_controls(driver)

        # Fill feedback form
        print("\n========== FILLING FEEDBACK FORM ==========")

        result = fill_feedback_form(driver, answer)

        print("\n========== FINAL STATUS ==========")

        if result and not result.get("errors"):
            print("Filling process completed.")
        else:
            print("Some controls could not be processed.")

        print("Please review every answer manually.")
        print("Comments have been left untouched.")
        print("No form has been submitted.")

        input("\nPress ENTER to close the browser...")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
