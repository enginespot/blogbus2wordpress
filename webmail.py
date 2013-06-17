import smtplib
import os

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

def send_mail(send_to, subject,files=[]):
    server = 'smtp.gmail.com'
    port = 587
    sender = ''#email address
    password=''#password
    recipient = send_to


#    assert type(send_to)==list
#    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = sender
#    msg['To'] = COMMASPACE.join(send_to)
    msg['To']=send_to
    msg['Date'] = formatdate(localtime=True)

    msg['Subject'] = subject
    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
#        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        part.add_header('Content-Disposition', 'attachment; filename=blogbus.zip')
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo
    smtp.login(sender, password)
    smtp.sendmail(sender, send_to, msg.as_string())
    smtp.close()

#send_mail('exceedream@gmail.com','hello world','hello',['temp.zip'])
