## Archive Files Script

This Python script `archive_files.py` is designed to create tar files of specified directories and send notifications via email and Slack upon completion or failure of the backup process.

### Installation

1. **Clone the Repository:** Clone the repository containing the `archive_files.py` script to your local environment.

2. **Python Dependencies:** Ensure that you have Python 3 installed on your system along with the required Python packages specified in the script. You can install these packages using pip:

    ```bash
    pip install tarfile requests
    ```

3. **Configuration:**

    - Update the script with your email and Slack credentials.
    - Replace the Slack webhook URL with your own Slack webhook URL.

4. **Cronjob Installation:**

    Add the following cronjob to your system's crontab to execute the script at regular intervals. This example schedules the script to run every minute.

    ```bash
    * * * * * /usr/bin/python3 /home/ubuntu/environment/archive_files.py
    ```

### Usage

Once installed and configured, the script will automatically create tar files of specified directories according to the cronjob schedule. Upon completion, it will send notifications via email and Slack.

### Script Overview

The script performs the following tasks:

- Creates tar files of specified directories.
- Sends notifications via email and Slack upon completion or failure of the backup process.

### Script Details

- **Logger Configuration:** The script is equipped with a logger to facilitate logging of messages at different levels.

- **Email Functionality:** The `send_email` function sends email notifications upon completion or failure of the backup process.

- **Slack Integration:** The `send_slack` function sends Slack notifications upon completion or failure of the backup process using a webhook URL.

- **Tar File Creation:** The script creates tar files of specified directories using the `tarfile` module in Python.

- **Cronjob:** The provided cronjob schedules the script to run at regular intervals. Adjust the cronjob timing according to your backup requirements.

### Notes

- Ensure that the specified directories exist and have the necessary permissions for the script to create tar files successfully.

- Customize the email and Slack notification messages according to your preferences.

- Monitor the cronjob execution and adjust the timing as needed based on your backup requirements.
