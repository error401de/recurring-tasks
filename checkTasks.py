import configparser, sendMail

config = configparser.ConfigParser()
config.read('tasks.ini')

for i in config.sections():
	taskType = config.get(i, 'Type')

	if taskType == 'daily':
		sendMail.sendNotification(i, config.get(i, 'Message'))
