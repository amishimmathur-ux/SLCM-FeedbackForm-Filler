
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

URL = "https://mujslcm.jaipur.manipal.edu/Student"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

driver.get(URL)

input("Login and open one pending feedback form. Press ENTER...")

time.sleep(3)

os.makedirs("logs", exist_ok=True)
os.makedirs("screenshots", exist_ok=True)

report = []

# Inspect buttons
report.append("========== BUTTONS ==========")

for i, button in enumerate(driver.find_elements(By.TAG_NAME, "button")):

    if button.is_displayed():
        report.append(
            f"Button {i}: Text={button.text.strip()}, "
            f"ID={button.get_attribute('id')}, "
            f"Class={button.get_attribute('class')}"
        )

# Inspect dropdowns
report.append("\n========== DROPDOWNS ==========")

for i, dropdown in enumerate(driver.find_elements(By.TAG_NAME, "select")):

    report.append(
        f"Dropdown {i}: ID={dropdown.get_attribute('id')}, "
        f"Name={dropdown.get_attribute('name')}"
    )

    for option in dropdown.find_elements(By.TAG_NAME, "option"):
        report.append("Option: " + option.text.strip())

# Inspect inputs
report.append("\n========== INPUTS ==========")

for i, element in enumerate(driver.find_elements(By.TAG_NAME, "input")):

    report.append(
        f"Input {i}: Type={element.get_attribute('type')}, "
        f"ID={element.get_attribute('id')}, "
        f"Name={element.get_attribute('name')}, "
        f"Value={element.get_attribute('value')}"
    )

# Inspect text areas
report.append("\n========== TEXT AREAS ==========")

for element in driver.find_elements(By.TAG_NAME, "textarea"):

    report.append(
        f"Textarea: ID={element.get_attribute('id')}, "
        f"Name={element.get_attribute('name')}"
    )

# Save report
with open("logs/form_inspection.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(report))

driver.save_screenshot("screenshots/form_inspection.png")

print("Screenshot saved in screenshots/form_inspection.png")


print("\nInspection completed!")
print("Report saved in logs/form_inspection.txt")

input("Press ENTER to close browser...")
driver.quit()
