import configparser, sendMail
from datetime import datetime

daysOfTheWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
monthsOfTheYear = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

config = configparser.ConfigParser()
config.read('tasks.ini')

now = datetime.now()
day = now.strftime("%d")
month = now.strftime("%m")

for i in config.sections():
	taskType = config.get(i, 'Type')

	if taskType == 'daily':
		sendMail.sendNotification(i, config.get(i, 'Message'))

	if taskType == 'weekly':
		for j in config.get(i, 'Weekday').split(','):
			if daysOfTheWeek.index(j) == now.weekday():
				sendMail.sendNotification(i, config.get(i, 'Message'))

	if taskType == 'monthly':
		for j in config.get(i, 'Day').split(','):
			if day == j:
				sendMail.sendNotification(i, config.get(i, 'Message'))

	if taskType == 'yearly':
		if config.get(i, 'Day') == day and monthsOfTheYear.index(config.get(i, 'Month')) + 1 == int(month):
			sendMail.sendNotification(i, config.get(i, 'Message'))

	if taskType == 'free':
		for j in config.get(i, 'Month').split(','):
			if monthsOfTheYear.index(j) + 1 == int(month):
				for k in config.get(i, 'Day').split(','):
					if day == k:
						sendMail.sendNotification(i, config.get(i, 'Message'))
