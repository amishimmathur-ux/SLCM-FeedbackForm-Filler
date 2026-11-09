
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from feedback_bot import fill_feedback_form, submit_feedback_form

import json
import time


URL = "https://mujslcm.jaipur.manipal.edu/Student"


def get_pending_forms(driver):

    print("\n========== SCANNING FEEDBACK FORMS ==========")

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

    answer = config.get("default_answer", "YES")

    if answer.strip().upper() not in ["YES", "NO"]:
        raise ValueError("default_answer must be YES or NO in config.json")

    answer = answer.strip().upper()

    # Start Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    filled_count = 0
    submitted_count = 0
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

        # Save the feedback list tab
        list_tab = driver.current_window_handle

        # Find pending forms
        pending_forms, completed_count = get_pending_forms(driver)

        if not pending_forms:

            print("\nNo pending forms found.")
            return

        print("\n========== FORMS TO BE PROCESSED ==========")

        for index, form in enumerate(pending_forms, start=1):

            print(f"\n{index}. {form['name']}")

        print("\nThe bot will:")
        print("1. Open each pending form in a new tab.")
        print("2. Fill the configured answers.")
        print("3. Verify the answers.")
        print("4. Submit forms that pass verification.")
        print("\nCompleted forms will be skipped.")

        input("\nPress ENTER to begin processing...")

        # Process each pending form
        for index, form in enumerate(pending_forms, start=1):

            print("\n========================================")
            print(f"PROCESSING FORM {index}/{len(pending_forms)}")
            print("========================================")

            print("Form:", form["name"])

            try:

                # Open questionnaire in a new tab
                previous_handles = set(driver.window_handles)

                driver.execute_script(
                    "window.open(arguments[0], '_blank');",
                    form["url"]
                )

                WebDriverWait(driver, 10).until(
                    lambda d: len(d.window_handles) > len(previous_handles)
                )

                new_tab = next(
                    handle for handle in driver.window_handles
                    if handle not in previous_handles
                )

                driver.switch_to.window(new_tab)

                # Wait for questionnaire to load
                WebDriverWait(driver, 20).until(
                    lambda d: d.execute_script(
                        "return document.readyState"
                    ) == "complete"
                )

                time.sleep(2)

                print("Questionnaire opened:", driver.current_url)

                # Fill the questionnaire
                result = fill_feedback_form(driver, answer)

                if not result or result.get("errors"):

                    failed_count += 1

                    print("\nFORM NEEDS MANUAL ATTENTION")
                    print("Submission skipped because filling errors were found.")

                    continue

                # Verify all detected radio questions were processed
                expected_questions = result["questions_detected"]

                processed_questions = (
                    result["selected"] +
                    result["already_selected"]
                )

                all_questions_filled = (
                    expected_questions > 0
                    and processed_questions == expected_questions
                )

                # Verify dropdowns too
                dropdown_count = len(
                    driver.find_elements(
                        By.CSS_SELECTOR,
                        "select[id^='dtPartYes']"
                    )
                )

                dropdowns_filled = result["dropdowns_filled"]

                all_dropdowns_filled = (
                    dropdown_count == dropdowns_filled
                    or all(
                        dropdown.is_enabled()
                        and bool(
                            dropdown.get_attribute("value")
                        )
                        for dropdown in driver.find_elements(
                            By.CSS_SELECTOR,
                            "select[id^='dtPartYes']"
                        )
                    )
                )

                if not all_questions_filled or not all_dropdowns_filled:

                    failed_count += 1

                    print("\nFORM INCOMPLETE")
                    print("Submission skipped.")
                    continue

                print("\nALL ANSWERS VERIFIED.")
                filled_count += 1

                # Automatically submit the questionnaire
                print("\nSubmitting form...")

                submitted = submit_feedback_form(driver)

                if submitted:

                    submitted_count += 1

                    print("\nSUBMISSION ACTION COMPLETED.")

                else:

                    failed_count += 1

                    print("\nSUBMISSION FAILED.")
                    print("Please check this form manually.")

                time.sleep(2)

            except Exception as error:

                failed_count += 1

                print("\nERROR PROCESSING FORM:")
                print(error)

            finally:

                # Return to feedback list tab
                if list_tab in driver.window_handles:

                    driver.switch_to.window(list_tab)

        # Final summary
        print("\n========================================")
        print("       BULK FEEDBACK BOT SUMMARY")
        print("========================================")

        print("Pending forms found:", len(pending_forms))
        print("Completed forms skipped:", completed_count)
        print("Forms filled:", filled_count)
        print("Submission actions completed:", submitted_count)
        print("Forms requiring attention:", failed_count)

        print("\nPlease check the portal to confirm")
        print("that submitted forms show Completed.")

        input("\nPress ENTER to close the browser...")

    finally:

        driver.quit()


if __name__ == "__main__":
    main()
