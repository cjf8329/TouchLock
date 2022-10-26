import smtplib
from email.message import EmailMessage


email_address = "touchlock.biolock@gmail.com"
email_password = "igxvftioggpjopgg"

# create email
msg = EmailMessage()
msg['Subject'] = "Email test"
msg['From'] = email_address
msg['To'] = "insert_email_here@gmail.com"
msg.set_content("https://www.youtube.com/watch?v=bmtHdZlsiO8")

# send email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_address, email_password)
    smtp.send_message(msg)
