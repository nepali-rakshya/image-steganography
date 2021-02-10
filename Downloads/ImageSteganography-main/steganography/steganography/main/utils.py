import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(email: str, image_name: str):
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    message = MIMEMultipart('alternative')
    message['Subject'] = "Your Encrypted Message "
    message['From'] = 'rakshyanepali440@gmail.com'
    message['To'] = email
    dir_path = os.path.join(APP_ROOT, 'static\\image')
    html = f"""\
    <html>
      <head></head>
      <body>
        <h1>Hidden Message</h1>
        <p>
           Here's your enocoded message in message
        </p>
      </body>
    </html>
    """
    attachment = MIMEApplication(open(image_name, "rb").read(), _subtype="txt")
    attachment.add_header('Content-Disposition',
                          'attachment', filename=image_name)
    message.attach(attachment)

    message.attach(MIMEText(html, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('rakshyanepali440@gmail.com', 'Password')
    server.sendmail("rakshyanepali440@gmail.com", email, message.as_string())
    server.quit()
