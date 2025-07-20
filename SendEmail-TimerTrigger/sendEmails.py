import os
from azure.cosmos import CosmosClient
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Cosmos DB setup
endpoint = os.environ.get('COSMOS_ENDPOINT')
key = os.environ.get('COSMOS_KEY')
database_id = os.environ.get('COSMOS_DATABASE')
container_id = os.environ.get('COSMOS_CONTAINER')

client = CosmosClient(endpoint, key)
database = client.get_database_client(database_id)
container = database.get_container_client(container_id)

# Gmail SMTP settings
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465
SMTP_USERNAME = os.environ.get('GMAIL_USERNAME')  # your Gmail address
SMTP_PASSWORD = os.environ.get('GMAIL_PASSWORD')  # your Gmail app password
SENDER_EMAIL = SMTP_USERNAME

def strip_html(html):
    # crude fallback plaintext version
    from bs4 import BeautifulSoup
    return BeautifulSoup(html, "html.parser").get_text()


# Determine path to scraped_content.txt
scrape_file_path = '/tmp/scraped_content.txt'
def extract_date_from_file():
    try:
        with open(scrape_file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if first_line.startswith("Date: "):
                return first_line.replace("Date: ", "")
    except Exception as e:
        print("Error reading date from file:", e)
    return None


def send_email_to_all_users(html_template):
    try:
        users = list(container.read_all_items())
    except Exception as e:
        print("Failed to fetch users from DB:", e)
        return

    date_str = extract_date_from_file()
    if date_str:
        subject = f"Yesterday's Anime News – {date_str}"
    else:
        subject = "Yesterday's Anime News"

    for user in users:
        email = user.get('email')
        user_id = user.get('id')

        if not email or not user_id:
            continue

        # Update this URL after deployment!
        unsub_link = f"https://your-server-url/api/unsubscribe/{user_id}"
        personalized_html = html_template.replace("{{UNSUB_LINK}}", unsub_link)
        plain_text = strip_html(personalized_html)

        msg = MIMEMultipart("alternative")
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = email

        msg.attach(MIMEText(plain_text, 'plain'))
        msg.attach(MIMEText(personalized_html, 'html'))

        try:
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.sendmail(SENDER_EMAIL, email, msg.as_string())
            print(f"Sent to {email}")
        except Exception as e:
            print(f"Failed to send to {email}: {e}")
