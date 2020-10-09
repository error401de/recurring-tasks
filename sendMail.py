import smtplib, ssl, configparser, sys

def sendNotification(subject, description):
	config = configparser.ConfigParser()
	config.read('config.ini')
	smtp_server = config.get('email', 'SmtpServer')
	port = config.get('email', 'SmtpPort')
	user = config.get('email', 'SmtpUser')
	password = config.get('email', 'SmtpPassword')
	sender = config.get('email', 'SmtpSender')
	recipient = config.get('email', 'MailRecipient')
	prefix = config.get('email', 'MailPrefix')
	headers = "From: %s\nTo: %s\nSubject: %s\n\n" % (sender, recipient, prefix + ' ' + subject)
	body = "Recurring task is due: " + description

	message = headers + body
	context = ssl.create_default_context()
	with smtplib.SMTP(smtp_server, port) as server:
		server.starttls(context=context)
		server.login(user, password)
		server.sendmail(sender,recipient, message)
