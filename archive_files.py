#!/usr/bin/python3
import tarfile
from datetime import datetime
import os
import smtplib
import requests
import json
from datetime import datetime
import logging

# Create a logger
logger = logging.getLogger(__name__)

# Create a console handler and set its logging level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and set its format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)

# Define email configs
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'davyngugi@gmail.com'
smtp_password = os.environ.get('SECRET_PASSWORD')

def send_email(subject, msg):
    from_email = 'davyngugi@gmail.com'
    to_email = 'team@deployguru.com'
    subject = subject
    body = msg

    message = f'Subject: {subject}\n\n{body}'
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(smtp_username, smtp_password)
            smtp.sendmail(from_email, to_email, message)
        logger.info("Email Successfully sent")
        
    except Exception as error:
        logger.exception(f'Something went Wrong\n {error}')
        
def send_slack(message_payload):
    # Replace the URL below with your Slack webhook URL
    webhook_url = 'https://hooks.slack.com/services/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'
        
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, data=json.dumps(message_payload), headers=headers)
    
    if response.status_code == 200:
        logger.info("Message sent successfully")
    else:
        logger.error(f"Failed to send message, status code: {response.status_code}")

def create_message(json_data):
    json_data = json.loads(json_data)
    # Parse the date-time string
    date_time_str = datetime.strptime(json_data['timestamp'], '%Y%m%d_%H%M%S')
    json_data['timestamp'] = date_time_str

    # Format the date-time object as human-readable format
    date_time_str = date_time_str.strftime('%B %d, %Y %I:%M:%S %p')

    #json_data = {'backup_by': user, 'time': date_time_str, 'source': source, 'archived_filename': filename}

    markdown_output = ""
    for key, value in json_data.items():
        markdown_output += f"{key}: {value}\n"


    json_data = {
        "text": "```Backup Information```",
        "blocks": [
            {
                "type": "rich_text",
                "elements": [
                    {
                        "type": "rich_text_preformatted",
                        "elements": [
                            {
                                "type": "text",
                                "text": markdown_output
                            }
                        ],
                        "border": 0
                    }
                ]
            }
        ]
    }

    return json_data

user = "Davy Ngugi"

# Get current date and time for the filename
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

# Specify the target directory for the tar files
target_directory = '/opt/backups'

# Specify source directory
source_directory = '/var/www/html'

# Create tar files for each folder
try:
    # successfully archived files
    archived = ""
    
    logger.debug(f" --- working on {source_directory}")
    
    # Append date and time to tar file name
    tar_file_name = f'html_files_{current_time}.tar'
    
    # Full path to the tar file
    tar_file_path = os.path.join(target_directory, tar_file_name)
         
    # Create tar file using the tarfile module
    with tarfile.open(tar_file_path, 'w') as tar:
        # Add all files in the folder to the tar file
        for root, _, files in os.walk(source_directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path)
                tar.add(file_path, arcname=arcname)
    
    logger.debug(f'Created {tar_file_name} in {target_directory}')
    
    json_data = json.dumps({'backup_by': user, 'timestamp': current_time, 'source': source_directory, 'archived_filename': os.path.join(target_directory, tar_file_name)}, indent=4)
    message = create_message(json_data)
    # Print a message when done
    logger.info(f'Tar files creation completed.\n{message}')
    send_email('Backup Successful by Davy Ngugi', json_data)
    #send_slack(message)
except Exception as e:
    logger.exception(f'\nFailed to create tar files \n {e}')
    send_email('Failed Backup by Davy Ngugi', 'Failed tp create tar files\n{e}')
    #send_slack(f'**Failed Backup by Davy Ngugi** \n Failed tp create tar files\n{e}')
