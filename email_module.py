import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class Emailer:

    def __init__(self, address, password):
        self.email_address = "touchlock.biolock@gmail.com"
        self.email_password = "igxvftioggpjopgg"
        self.message_to_send = None

    def create_email(self, mail_text, recipient, attachment=None):
        # create email header and text
        msg = MIMEMultipart()
        msg['Subject'] = "Email test"
        msg['From'] = self.email_address
        msg['To'] = recipient
        msg.attach(MIMEText(mail_text, 'plain'))

        #read image file
        if attachment is None:
            self.message_to_send = msg
            return

        file_name = attachment
        attached_file = open(file_name, 'rb')

        #attach image
        payload = MIMEBase("application", 'image')
        payload.set_payload((attached_file).read())
        encoders.encode_base64(payload)
        payload.add_header("Content-Disposition", "attachment", filename=file_name)
        msg.attach(payload)
        self.message_to_send = msg

    def send_email(self):
        # send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.email_address, self.email_password)
            smtp.send_message(self.message_to_send)
