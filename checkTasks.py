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

	if taskType == 'weekdayofmonth':
	for j in config.get(i, 'Weekday').split(','):
		for occurrence in config.get(i, 'Occurrence').split(','):
			if daysOfTheWeek.index(j) == now.weekday():
				if occurrence.lower() == "first" and 1 <= int(day) <= 7:
					sendMail.sendNotification(i, config.get(i, 'Message'))
				elif occurrence.lower() == "second" and 8 <= int(day) <= 14:
					sendMail.sendNotification(i, config.get(i, 'Message'))
				elif occurrence.lower() == "third" and 15 <= int(day) <= 21:
					sendMail.sendNotification(i, config.get(i, 'Message'))
				elif occurrence.lower() == "fourth" and 22 <= int(day) <= 28:
					sendMail.sendNotification(i, config.get(i, 'Message'))
				elif occurrence.lower() == "last" and 25 <= int(day) <= 31:
					sendMail.sendNotification(i, config.get(i, 'Message'))
				else:
					continue

	if taskType == 'yearly':
		if config.get(i, 'Day') == day and monthsOfTheYear.index(config.get(i, 'Month')) + 1 == int(month):
			sendMail.sendNotification(i, config.get(i, 'Message'))

	if taskType == 'free':
		for j in config.get(i, 'Month').split(','):
			if monthsOfTheYear.index(j) + 1 == int(month):
				for k in config.get(i, 'Day').split(','):
					if day == k:
						sendMail.sendNotification(i, config.get(i, 'Message'))
