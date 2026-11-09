
# ⚡ SLCM Automatic Feedback Form Filler

<p align="center">
  <b>A Python-based browser automation tool for filling multiple MUJ SLCM feedback forms.</b>
</p>

<p align="center">
  ![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python) <br>
  ![Selenium](https://img.shields.io/badge/Selenium-Automation-green?logo=selenium)<br>
  ![Chrome](https://img.shields.io/badge/Browser-Google%20Chrome-yellow?logo=googlechrome)<br>
  ![License](https://img.shields.io/badge/License-MIT-orange)<br>
  ![Status](https://img.shields.io/badge/Status-Active-success)<br>
</p>

---

## About The Project

**SLCM Automatic Feedback Form Filler** is a Python automation project developed to simplify repetitive feedback form interactions on the Manipal University Jaipur (MUJ) Student Learning and Course Management (SLCM) portal.

The project uses **Selenium WebDriver** to automate browser interactions, identify pending feedback forms, fill supported questionnaire controls, verify selections, and attempt automatic submission.

Instead of manually opening and filling every feedback form, the bot processes multiple pending forms in one execution.

### Project Objectives

- Reduce repetitive manual work.
- Automate the detection of pending feedback forms.
- Fill supported Yes/No radio buttons and dropdowns.
- Process multiple feedback forms automatically.
- Reduce errors through answer verification.
- Simplify the feedback form workflow.

---

## Features

| Feature | Description |
|---|---|
|  Pending Form Detection | Automatically identifies pending feedback forms. |
|  Completed Form Skipping | Skips forms that are already completed. |
|  Multiple Form Processing | Opens multiple pending forms in separate browser tabs. |
|  Radio Button Automation | Automatically selects configured Yes/No answers. |
|  Dropdown Automation | Handles supported Yes/No dropdown questions. |
|  Answer Verification | Checks whether detected questions have selected answers. |
|  Automatic Submission | Attempts to submit forms after filling checks pass. |
|  Terminal Summary | Displays the processing and submission counts. |
|  Manual Login | Allows users to log in themselves without storing portal passwords. |

---

## Tech Stack

- **Python 3** – Core programming language.
- **Selenium WebDriver** – Browser automation.
- **Google Chrome** – Browser used for automation.
- **JSON** – Stores the default answer configuration.

---

## Project Structure

```text
slcmAutomaticFeedbackFormFiller/
│
├── main.py
│   └── Main program: login workflow, pending form detection,
│       multiple form processing and submission.
│
├── feedback_bot.py
│   └── Handles radio buttons, dropdowns, verification
│       and Submit button interaction.
│
├── config.json
│   └── Stores the default Yes/No answer.
│
├── requirements.txt
│   └── Python dependencies.
│
├── .gitignore
│   └── Excludes unnecessary and sensitive files.
│
├── LICENSE
│   └── MIT License.
│
└── README.md
    └── Project documentation.
```

---

## Installation & Setup

Follow these steps to install and configure the project.

### 1. Prerequisites

Make sure you have:

- Python 3.10 or newer.
- Google Chrome installed.
- Visual Studio Code (recommended).
- Access to the MUJ SLCM portal.
- An active internet connection.

Check Python installation:

```bash
python --version
```

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

Navigate into the project directory:

```bash
cd YOUR-REPOSITORY
```

Replace `YOUR-USERNAME` and `YOUR-REPOSITORY` with your GitHub details.

### 3. Create a Virtual Environment

For Windows:

```bash
python -m venv .venv
```

Activate it using PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or using Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

If you do not have a requirements file yet:

```bash
python -m pip install selenium
```

### 5. Configure the Bot

Open `config.json`.

Example:

```json
{
    "default_answer": "YES"
}
```

You can configure:

- `"YES"` – Selects Yes for supported Yes/No questions.
- `"NO"` – Selects No for supported Yes/No questions.

**Important:** Choose answers that genuinely reflect your experience. The same configured answer is applied broadly by the current implementation.

---

## How To Operate The Project

This section explains how to run the bot from start to finish.

### Step 1: Open the Project

Open the project folder in Visual Studio Code.

### Step 2: Activate the Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Configure Your Answer

Open `config.json` and select your intended default answer:

```json
{
    "default_answer": "YES"
}
```

### Step 4: Run the Main Program

In the VS Code terminal, execute:

```bash
python main.py
```

### Step 5: Log In to MUJ SLCM

A Google Chrome window will open.

1. Log in to your MUJ SLCM account manually.
2. Navigate to the Feedback List page.
3. Make sure the feedback forms table is visible.
4. Return to the VS Code terminal.
5. Press ENTER when prompted.

### Step 6: Pending Forms Detection

The bot scans the feedback table and identifies:

- Pending feedback forms.
- Already completed feedback forms.

Completed forms are automatically skipped.

The bot displays the list of pending forms before starting.

### Step 7: Automatic Form Filling

After you press ENTER, the bot:

1. Opens a pending feedback form in a new browser tab.
2. Waits for the questionnaire to load.
3. Detects supported Yes/No radio buttons.
4. Selects the configured answer.
5. Fills supported Yes/No dropdown questions.
6. Verifies the selected answers.
7. Checks for filling errors.

### Step 8: Automatic Submission

If the filling checks pass, the bot locates the Submit button and attempts to click it.

Forms with detected errors or incomplete supported controls are skipped for submission.

### Step 9: Final Summary

After processing all detected forms, the terminal displays a summary.

Example:

```text
========== BULK FEEDBACK BOT SUMMARY ==========

Pending forms found: 4
Completed forms skipped: 4
Forms filled: 4
Submission actions completed: 4
Forms requiring attention: 0
```

*The numbers above are illustrative.*

Check the SLCM portal afterwards to confirm that submitted forms are actually marked Completed.

### Step 10: Close the Browser

Press ENTER when prompted to close the browser and finish execution.

---

## How The Project Works

The project is divided into two primary Python modules.

### 1. main.py

The main controller of the automation system.

Responsibilities:

- Loads the configuration file.
- Initializes the Chrome WebDriver.
- Waits for manual login.
- Scans the feedback list.
- Identifies pending and completed forms.
- Opens pending forms in separate tabs.
- Calls the feedback filling function.
- Calls the submission function.
- Generates the final processing summary.

### 2. feedback_bot.py

Contains the core feedback automation logic.

Responsibilities:

- Locates radio-button labels.
- Groups Yes/No radio buttons by their input names.
- Selects the configured answer.
- Avoids overwriting existing selections.
- Handles supported dropdown questions.
- Verifies selected answers.
- Detects and reports errors.
- Locates and clicks the Submit button.

### 3. config.json

Stores the default answer used by the automation.

Example:

```json
{
    "default_answer": "YES"
}
```

This makes it possible to change the configured answer without modifying the Python source code.

---

## Security & Privacy

Security is important when automating a student portal.

- The bot does not require your SLCM password in the source code.
- Login is performed manually by the user.
- Do not upload passwords, session cookies, authentication tokens, or browser profiles to GitHub.
- Keep virtual environments and temporary files out of version control.
- Never commit private student information.

---

## Limitations & Important Notes

- The current scanner processes feedback rows rendered on the currently visible feedback-list page. Pagination is not implemented.
- The automation supports the radio-button and dropdown structures identified in the current MUJ feedback forms.
- Changes to the SLCM website may require changes to Selenium selectors.
- The current configuration applies one default answer broadly. It does not evaluate the actual quality of a course or instructor.
- The bot's submission function confirms that it attempted to click Submit. It does not independently verify that the server saved the feedback.
- Always check the portal after execution to confirm the final status.
- Use truthful answers and follow your institution's policies.

---

## Troubleshooting

### Error: No module named selenium

Run:

```bash
python -m pip install selenium
```

### Chrome Does Not Open

- Check whether Google Chrome is installed.
- Ensure the virtual environment is activated.
- Update Selenium:

```bash
python -m pip install --upgrade selenium
```

### No Pending Forms Found

- Make sure you are on the Feedback List page.
- Ensure the feedback table is visible.
- Check whether the forms are on another pagination page.
- Check whether the portal's HTML structure has changed.

### Some Forms Are Skipped

Check the terminal output for errors.

A form may be skipped if:

- A Yes/No option cannot be located.
- A radio button cannot be selected.
- A dropdown cannot be filled.
- The page structure has changed.
- The supported controls are incomplete.

### Submit Button Not Found

The portal may have changed its button structure. Inspect the questionnaire and update the selector in `submit_feedback_form()` if necessary.

---

## Contributing

Contributions are welcome!

If you would like to improve this project:

1. Fork this repository.
2. Create a new branch.
3. Make your changes.
4. Test your implementation.
5. Submit a pull request.

Please do not include passwords, cookies, private student information, or other sensitive data in contributions.

---

## License

This project is licensed under the **MIT License**.

You are free to use, modify, distribute, and share this project under the terms of the MIT License.

See the [LICENSE](LICENSE) file for more information.

---

## Author

**Amishi Mathur**

GitHub: [@amishimmathur-ux](https://github.com/amishimmathur-ux)

---

