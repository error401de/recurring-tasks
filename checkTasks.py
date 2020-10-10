import configparser, sendMail
from datetime import datetime

taskTypeList = ["daily", "weekly", "monthly", "weekdayofmonth", "yearly", "free"]
daysOfTheWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
monthsOfTheYear = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                   "November", "December"]
occurrences = ["first", "second", "third", "fourth", "last"]

config = configparser.ConfigParser()
config.read('tasks.ini')

now = datetime.now()
day = now.strftime("%d")
month = now.strftime("%m")

def validate_task_type(tt):
    if tt not in taskTypeList:
        raise ValueError("Sorry, taskType should only be in {}".format(taskTypeList))

def validate_weekday(wd):
    if wd not in daysOfTheWeek:
        raise ValueError("Sorry, Weekday should only be in {}".format(daysOfTheWeek))

def validate_month(m):
    if m not in monthsOfTheYear:
        raise ValueError("Sorry, month should only be in  {}".format(monthsOfTheYear))
        
def validate_occurrence(o):
    if o not in occurrences:
        raise ValueError("Sorry, occurrence should only be in {}".format(occurrences))

def validate_day(d):
    try:
        d = int(d)
    except:
        raise ValueError("day should be an int")
    if d < 1 or d > 31:
        raise ValueError("Sorry, day should only be in  [1, 31]")

for i in config.sections():
    taskType = config.get(i, 'Type')
    validate_task_type(taskType)

    if taskType == 'daily':
        sendMail.sendNotification(i, config.get(i, 'Message'))

    if taskType == 'weekly':
        for j in config.get(i, 'Weekday').split(','):
            validate_weekday(j)
            if daysOfTheWeek.index(j) == now.weekday():
                sendMail.sendNotification(i, config.get(i, 'Message'))

    if taskType == 'monthly':
        for j in config.get(i, 'Day').split(','):
            validate_day(j)
            if day == j:
                sendMail.sendNotification(i, config.get(i, 'Message'))
                
    if taskType == 'weekdayofmonth':
        for j in config.get(i, 'Weekday').split(','):
            validate_weekday(j)
            for occurrence in config.get(i, 'Occurrence').split(','):
                validate_occurrence(occurrence):
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
        m = config.get(i, 'Month')
        d = config.get(i, 'Day')
        if len(list(month.split(','))) > 1 or len(list(d.split(','))) > 1:
            raise ValueError("Sorry, yearly task should only contain one specific date")
        validate_day(d)
        validate_month(m)
        if day == d and monthsOfTheYear.index(m) + 1 == int(month):
            sendMail.sendNotification(i, config.get(i, 'Message'))

    if taskType == 'free':
        for j in config.get(i, 'Month').split(','):
            validate_month(j)
            if monthsOfTheYear.index(j) + 1 == int(month):
                for k in config.get(i, 'Day').split(','):
                    validate_day(k)
                    if day == k:
                        sendMail.sendNotification(i, config.get(i, 'Message'))
