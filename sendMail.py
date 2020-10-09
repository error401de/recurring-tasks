import smtplib, ssl, configparser, sys

config = configparser.ConfigParser()
config.read('config.ini')
smtp_server = config.get('email', 'SmtpServer')
port = config.get('email', 'SmtpPort')
user = config.get('email', 'SmtpUser')
password = config.get('email', 'SmtpPassword')
sender = config.get('email', 'SmtpSender')
recipient = config.get('email', 'MailRecipient')
message = f"""\
Subject: Recurring task: {sys.argv[1]}
To: {recipient}
From: {sender}

Recurring task is due: {sys.argv[2]}"""

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
	server.starttls(context=context)
	server.login(user, password)
	server.sendmail(sender,recipient, message)