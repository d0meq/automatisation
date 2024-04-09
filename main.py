import imaplib
import email
from email.header import decode_header

# IMAP server credentials
username = "your_email@gmail.com"
password = "uourpassword"

# IMAP server hostname (if other mail client use their imap server)
imap_host = "imap.gmail.com"

# Create IMAP connection
imap = imaplib.IMAP4_SSL(imap_host)

# Login to the email account
imap.login(username, password)

# Select the mailbox (inbox)
status, messages = imap.select("INBOX")

# Search for emails from the specified sender
sender_email = input("Input an sender email: ")
status, search_result = imap.search(None, f'(FROM "{sender_email}")')

# Get list of message IDs
message_ids = search_result[0].split()

# Iterate through each message and delete it
for message_id in message_ids:
    # Delete the message
    imap.store(message_id, '+FLAGS', '\\Deleted')

# Expunge the deleted messages
imap.expunge()

# Logout from the email account
imap.logout()

print(f"Deleted {len(message_ids)} emails from {sender_email}.")