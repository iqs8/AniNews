import logging
import azure.functions as func
from dotenv import load_dotenv
from scrape import scrape_news
from apiCall import generate_html
from sendEmails import send_email_to_all_users
import os
import tempfile


import datetime
load_dotenv()

app = func.FunctionApp()

def send_newsletter():
    logging.info("Timer function started")

    # Scrape news and get content
    scrape_news()

    # Check temp file details
    temp_path = os.path.join(tempfile.gettempdir(), 'scraped_content.txt')
    try:
        with open(temp_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            num_lines = len(lines)
            content = ''.join(lines)
            num_titles = content.count("Title")
        logging.info(f"scraped_content.txt: {num_lines} lines, 'Title' appears {num_titles} times.")
    except Exception as e:
        logging.error(f"Could not read temp file: {e}")

        
    # Generate HTML newsletter
    html_newsletter = generate_html()
    # Send emails
    send_email_to_all_users(html_newsletter)
    logging.info("Newsletter generated and sent.")

@app.function_name(name="newsletterSenderFunction")
@app.timer_trigger(schedule="0 0 11 * * *",  # Every day at 11:00 AM UTC, 7 AM EST
                   arg_name="myTimer", 
                   run_on_startup=False,   #set this back to false after
                   use_monitor=False) 
def newsletterSenderFunction(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')

    
    try:
        send_newsletter()
    except Exception as e:
        import traceback
        print("Exception occurred:", e)
        print(traceback.format_exc())