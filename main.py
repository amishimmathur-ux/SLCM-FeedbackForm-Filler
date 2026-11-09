
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from feedback_bot import fill_feedback_form
import json
import time

URL = "https://mujslcm.jaipur.manipal.edu/Student"


def get_pending_forms(driver):

    print("\n========== SCANNING FEEDBACK FORMS ==========")

    # Read all visible table rows
    rows = driver.execute_script("""
        return Array.from(
            document.querySelectorAll("table tbody tr")
        ).map(row => {
            const link = row.querySelector("a");

            return {
                text: row.innerText,
                linkText: link ? link.innerText.trim() : "",
                href: link ? link.href : ""
            };
        });
    """)

    pending_forms = []
    completed_count = 0

    for row in rows:

        status = row["linkText"].strip().lower()

        if status == "pending" and "FeedbackId=" in row["href"]:

            pending_forms.append({
                "name": row["text"].replace("\n", " | "),
                "url": row["href"]
            })

        elif status == "completed":

            completed_count += 1

    print("Completed forms:", completed_count)
    print("Pending forms:", len(pending_forms))

    return pending_forms, completed_count


def main():

    # Load configuration
    with open("config.json", "r") as file:
        config = json.load(file)

    answer = config.get("default_answer", "Yes")

    # Open Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    filled_count = 0
    failed_count = 0

    try:

        driver.get(URL)

        print("\n========== MUJ BULK FEEDBACK BOT ==========")

        input(
            "\n1. Log in to SLCM."
            "\n2. Navigate to the Feedback List page."
            "\n3. Make sure the forms table is visible."
            "\n4. Press ENTER to start..."
        )

        time.sleep(2)

        # Remember the feedback list tab
        list_tab = driver.current_window_handle

        # Find all pending forms
        pending_forms, completed_count = get_pending_forms(driver)

        if not pending_forms:

            print("\nNo pending forms found.")
            return

        print("\n========== FORMS TO BE PROCESSED ==========")

        for index, form in enumerate(pending_forms, start=1):
            print(f"{index}. {form['name']}")

        print("\nThe bot will open each pending form in a NEW TAB.")
        print("Completed forms will be skipped.")
        print("No form will be submitted automatically.")

        input("\nPress ENTER to begin filling...")

        # Process each pending form
        for index, form in enumerate(pending_forms, start=1):

            print("\n========================================")
            print(f"PROCESSING FORM {index}/{len(pending_forms)}")
            print("========================================")

            print("Form:", form["name"])

            try:

                # Open questionnaire in a separate tab
                driver.execute_script(
                    "window.open(arguments[0], '_blank');",
                    form["url"]
                )

                # Switch to newly opened tab
                driver.switch_to.window(driver.window_handles[-1])

                # Wait for page to load
                WebDriverWait(driver, 20).until(
                    lambda d: d.execute_script(
                        "return document.readyState"
                    ) == "complete"
                )

                time.sleep(2)

                print("Questionnaire opened:", driver.current_url)

                # Fill the questionnaire
                result = fill_feedback_form(driver, answer)

                if result and not result.get("errors"):

                    filled_count += 1

                    print("\nFORM FILLED SUCCESSFULLY")

                else:

                    failed_count += 1

                    print("\nFORM NEEDS MANUAL ATTENTION")

                print("Please review this questionnaire.")
                print("This tab will remain open.")
                print("The bot will NOT submit it.")

            except Exception as error:

                failed_count += 1

                print("\nERROR PROCESSING FORM:")
                print(error)

            time.sleep(1)

        # Return focus to feedback list
        driver.switch_to.window(list_tab)

        print("\n========== BULK FILLING SUMMARY ==========")

        print("Pending forms found:", len(pending_forms))
        print("Completed forms skipped:", completed_count)
        print("Forms filled without reported errors:", filled_count)
        print("Forms requiring attention:", failed_count)

        print("\nAll opened questionnaire tabs have been kept open.")
        print("Please review each form manually.")
        print("Submit forms yourself only after reviewing them.")

        input("\nPress ENTER to close the browser...")

    finally:

        driver.quit()


if __name__ == "__main__":
    main()
