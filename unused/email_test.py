import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


mail_text = 'dfhfxchgxdggdx Balls'

email_address = "touchlock.biolock@gmail.com"
email_password = "igxvftioggpjopgg"

# create email header and text
msg = MIMEMultipart()
msg['Subject'] = "Email test"
msg['From'] = email_address
msg['To'] = "karantsukheja@gmail.com"
msg.attach(MIMEText(mail_text, 'plain'))

#attach image
file_name = 'ball.png'
attached_file = open(file_name, 'rb')

payload = MIMEBase("application", 'image')
payload.set_payload((attached_file).read())
encoders.encode_base64(payload)
payload.add_header("Content-Disposition", "attachment", filename=file_name)
msg.attach(payload)

# send email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_address, email_password)
    smtp.send_message(msg)
