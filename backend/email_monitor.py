import imaplib
import re
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import email
from config import Config
from sqlalchemy.exc import IntegrityError
from rfq_generator import generate_rfq_table
from agent_rfq import get_supplier_info, parse_supplier_info

from models import Email, SessionLocal

def check_email():
    mail = imaplib.IMAP4_SSL(Config.EMAIL_HOST)
    mail.login(Config.EMAIL_USER, Config.EMAIL_PASS)
    mail.select('Inbox')

    status, data = mail.search(None, 'ALL')
    mail_ids = data[0].split()

    emails = []
    session = SessionLocal()

    for mail_id in mail_ids:
        status, data = mail.fetch(mail_id, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Extract email details
        message_id = msg['Message-ID']  # Unique message ID
        print(message_id)
        subject = msg['Subject']
        print(subject)

        if re.search(r'\b(RFQ|Request for Quotation|Request for Quote)\b', subject, re.IGNORECASE):
            
            # Extract the body
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()

            # Check if the email with this Message-ID already exists
            existing_email = session.query(Email).filter_by(message_id=message_id).first()
            if existing_email:
                continue  # Skip if this email is already stored

            template_table = generate_rfq_table(body)
            print(f'Template Table: {template_table}')
            template_json = parse_supplier_info(get_supplier_info(email_content=body))
            print(f'Template JSON: {template_json}')

            # Create a new Email entry
            new_email = Email(
                message_id=message_id,
                subject=subject,
                body=body,
                template_table=template_table,
                template_json=template_json
            )

            # Save to the database
            try:
                session.add(new_email)
                session.commit()
            except IntegrityError:
                session.rollback()  # Handle the case where a duplicate Message-ID slipped through
            finally:
                emails.append(new_email)

        session.close()
    return emails


# template_md = """
#         **Gearbox:**
        
#         - TechNova Solutions | contact@technovasolutions.com
#         - GreenLeaf Industries | info@greenleafind.com
#         - Skyline Manufacturing | sales@skylinemfg.com
#         - BlueWave Technologies | support@bluewavetech.com
#         - Apex Global Logistics | inquiry@apexgloballogistics.com

#         **Electronics:**
        
#         - Tech Innovators | contact@techinnovators.com
#         - Global Circuits | sales@globalcircuits.com
#         - ElectroHub | info@electrohub.com
#         - Smart Devices Co. | support@smartdevices.com
#         - Circuit Masters | orders@circuitmasters.com
#         """



def extract_emails(url):
    # Set a custom User-Agent to mimic a web browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # Send a GET request to the URL with custom headers
        response = requests.get(url, headers=headers, timeout=10)
        
        # Raise an exception for bad status codes
        response.raise_for_status()

    except RequestException as e:
        print(f"Failed to retrieve the webpage: {e}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'lxml')

    # Find all text in the HTML
    text = soup.get_text()
    print(text)

    # Use regex to find email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)

    return emails

# Example usage
if __name__ == "__main__":
    # check_email()
    # url = input("Enter the URL to scrape for emails: ")
    url = "https://andsterengineering.com"
    emails = extract_emails(url)
    
    if emails:
        print("Emails found:")
        for email in emails:
            print(email)
    else:
        print("No emails found on the page.")