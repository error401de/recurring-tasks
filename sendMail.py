import smtplib, ssl, configparser, sys, os

def sendNotification(subject, description):
	path = os.path.dirname(os.path.abspath(__file__))
	config = configparser.ConfigParser()
	config.read(path + '/config.ini')
	smtp_server = config.get('email', 'SmtpServer')
	port = config.get('email', 'SmtpPort')
	user = config.get('email', 'SmtpUser')
	password = config.get('email', 'SmtpPassword')
	sender = config.get('email', 'SmtpSender')
	recipient = config.get('email', 'MailRecipient')
	prefix = config.get('email', 'MailPrefix')
	headers = "From: %s\nTo: %s\nSubject: %s\n\n" % (sender, recipient, prefix + ' ' + subject)
	body = "Recurring task is due: " + description
	if subject == 'Error':
		body = "Error: " + description

	message = headers + body
	context = ssl.create_default_context()

	if config.get('email', 'EncryptionMode') == '2':
		with smtplib.SMTP(smtp_server, port) as server:
			server.starttls(context=context)
			if config.get('email', 'SmtpUser'):
				server.login(user, password)
			server.sendmail(sender, recipient, message)

	if config.get('email', 'EncryptionMode') == '1':
		with smtplib.SMTP_SSL(smtp_server, port) as server:
			if config.get('email', 'SmtpUser'):
				server.login(user, password)
			server.sendmail(sender, recipient, message)

	if config.get('email', 'EncryptionMode') == '0':
		with smtplib.SMTP(smtp_server, port) as server:
			server.ehlo()
			if config.get('email', 'SmtpUser'):
				server.login(user, password)
			server.sendmail(sender, recipient, message)
