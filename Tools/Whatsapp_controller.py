import pywhatkit as kit
import Tools.contacts as c
import time
# Get the current time
import time
import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
contact = c.contact
contacts = contact.keys()

# Add email contacts
email_contact = c.email
email_contacts = email_contact.keys()
# print(email_contacts)


def chat_handler(a, b,c):
    platform = c.lower()
    if platform.lower() == "whatsapp":
        return whats_app(a, b)
    elif platform.lower() == "email":

        return send_email(a, b)
    else:
        return "❌ Unknown platform specified."


def whats_app(a,b):
    print(f"text initializing.......{a,b}")
    reciver = a.lower()
    print(reciver)
    if (reciver in contact):
        current_time = time.localtime()
        current_hour = current_time.tm_hour
        current_minute = current_time.tm_min + 1  # Add one minute
        if current_minute == 60:
            current_minute = 0
            current_hour += 1

        try:
            reciver = (contact.get(reciver))
            kit.sendwhatmsg(reciver,b, current_hour, current_minute)
            print("Message scheduled successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    else:
        print("well shit")  

    return b 

#whats_app("Text didi whatsup ?")




# AI-generated content (can be replaced with AI models)
def send_email(a,b):
    reciver = a.lower()
    print(reciver)
    sender_email = "bhadrakrishnayan@gmail.com"#input("📧 PLEASE ENTER YOUR EMAIL ID: ").strip()
    sender_password = "yitxlvmnyqqggoct"#input("🔐 PLEASE ENTER YOUR PASSWORD: ").strip()
                        #"officialshounak117@gmail.com"#input("📨 ENTER THE RECEIVER'S EMAIL ID: ").strip()

    if (reciver in email_contact):
            recipient_email = (email_contact.get(reciver))
            print(reciver)
    else:
        print("well shit")  

    subject = b[10]
    body = b
    
    # SMTP setup (Gmail SMTP server)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create an email message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        try:
            server.login(sender_email, sender_password)
        except smtplib.SMTPAuthenticationError:
            print("Authentication failed. Check your email and password or app password.")
            return
        except Exception as e:
            print("Login failed:", e)
            return

        try:
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print("✅ Email sent successfully!")
        except Exception as e:
            print("Failed to send email:", e)
        finally:
            server.quit()
    except Exception as e:
        print("Connection to SMTP server failed:", e)
    return a
# Function to read unread emails
def read_emails(email_user, email_pass):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, email_pass)
        mail.select("inbox")

        status, messages = mail.search(None, 'UNSEEN')
        if status != 'OK':
            print("No unread emails found or search failed.")
            return

        email_ids = messages[0].split()

        if not email_ids:
            print("📭 No new unread emails.")
            return

        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            if status != 'OK':
                print(f"Failed to fetch email with ID {email_id}")
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    try:
                        msg = email.message_from_bytes(response_part[1])
                        print("\n📩 From:", msg["From"])
                        print("Subject:", msg["Subject"])
                        print("Body:", msg.get_payload(decode=True).decode())
                    except Exception as e:
                        print("Error reading an email:", e)

        mail.logout()
    except imaplib.IMAP4.error as e:
        print("IMAP error:", e)
    except Exception as e:
        print("Failed to read emails:", e)

# # Example Usage
if __name__ == "__main__":

    try:
        # Send an email
        # send_email("sender_email", 'asfkj')
        chat_handler("Shounak", "hellow",'email')

        # Uncomment to read unread emails
        # read_emails(sender_email, sender_password)

    except ValueError as ve:
        print("Input Error:", ve)
    except Exception as e:
        print("Unexpected error:", e)