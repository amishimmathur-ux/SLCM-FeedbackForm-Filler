from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    WebDriverException
)


def fill_feedback_form(driver, answer="YES"):

    answer = answer.strip().upper()

    if answer not in ["YES", "NO"]:
        raise ValueError("Answer must be YES or NO")

    print("\n========== FILLING FEEDBACK FORM ==========")

    questions = {}
    selected = 0
    already_selected = 0
    dropdowns_filled = 0
    errors = []

    # Find visible labels containing hidden radio buttons
    labels = driver.find_elements(
        By.XPATH,
        "//label[.//input[@type='radio']]"
    )

    # Group labels by their radio button name
    for label in labels:
        try:
            radio = label.find_element(
                By.CSS_SELECTOR,
                "input[type='radio']"
            )

            name = radio.get_attribute("name")
            text = label.text.strip().upper()

            if name and text in ["YES", "NO"]:
                if name not in questions:
                    questions[name] = {}

                questions[name][text] = (label, radio)

        except Exception as error:
            errors.append(str(error))

    print("Questions detected:", len(questions))

    # Fill radio-button questions
    for name, options in questions.items():

        try:
            if answer not in options:
                errors.append(f"{name}: {answer} option not found")
                continue

            # Do not overwrite an existing answer
            existing = [
                radio
                for label, radio in options.values()
                if radio.is_selected()
            ]

            if existing:
                already_selected += 1
                continue

            target_label, target_radio = options[answer]

            # Scroll the answer into the centre of the screen
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                target_label
            )

            time.sleep(0.3)

            # Click the visible label
            target_label.click()

            # Verify the intended radio was selected
            if target_radio.is_selected():
                selected += 1
            else:
                errors.append(
                    f"{name}: Selection could not be verified"
                )

        except Exception as error:
            errors.append(f"{name}: {str(error)}")

    # Fill the two Yes/No dropdown questions
    dropdowns = driver.find_elements(
        By.CSS_SELECTOR,
        "select[id^='dtPartYes']"
    )

    dropdown_value = "Y" if answer == "YES" else "N"
    dropdown_text = "Yes" if answer == "YES" else "No"

    for dropdown in dropdowns:

        try:
            if not dropdown.is_enabled():
                continue

            select = Select(dropdown)

            # Leave existing answers unchanged
            if select.first_selected_option.get_attribute("value"):
                continue

            select.select_by_value(dropdown_value)

            if select.first_selected_option.get_attribute("value") == dropdown_value:
                dropdowns_filled += 1
            else:
                errors.append(
                    f"{dropdown.get_attribute('id')}: Verification failed"
                )

        except Exception as error:
            errors.append(str(error))

    print("\n========== FILLING SUMMARY ==========")
    print("Questions detected:", len(questions))
    print("New radio selections:", selected)
    print("Already selected:", already_selected)
    print("Dropdowns filled:", dropdowns_filled)
    print("Errors:", len(errors))

    for error in errors:
        print("Error:", error)

    print("=====================================")

    return {
        "questions_detected": len(questions),
        "selected": selected,
        "already_selected": already_selected,
        "dropdowns_filled": dropdowns_filled,
        "errors": errors
    }

def debug_controls(driver):

    print("\n========== PAGE DIAGNOSTICS ==========")

    print("Current URL:", driver.current_url)
    print("Page title:", driver.title)

    # Check if the page contains frames
    frames = driver.find_elements(By.TAG_NAME, "iframe")
    print("\nNumber of iframes:", len(frames))

    # Inspect radio buttons in the current document
    radios = driver.find_elements(
        By.XPATH,
        "//input[@type='radio']"
    )

    print("\nRadio buttons found:", len(radios))

    for i, radio in enumerate(radios):
        try:
            print(f"\nRadio {i + 1}")
            print("Name:", radio.get_attribute("name"))
            print("Value:", radio.get_attribute("value"))
            print("ID:", radio.get_attribute("id"))
            print("Displayed:", radio.is_displayed())
            print("Selected:", radio.is_selected())
            print("HTML:", radio.get_attribute("outerHTML"))

        except Exception as e:
            print("Error:", e)

    # Inspect labels
    labels = driver.find_elements(By.TAG_NAME, "label")

    print("\nLabels found:", len(labels))

    for i, label in enumerate(labels):
        try:
            text = label.text.strip()

            if text:
                print(f"Label {i + 1}: {text}")
                print("HTML:", label.get_attribute("outerHTML")[:500])

        except Exception:
            continue

    print("\n========== DIAGNOSTICS COMPLETE ==========")