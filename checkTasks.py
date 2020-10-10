import configparser, sendMail
from datetime import datetime
import logging

logging.basicConfig(level='DEBUG', filename='logs/app.log', filemode='a', format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')

taskTypeList = ["daily", "weekly", "monthly", "yearly", "free"]
daysOfTheWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
monthsOfTheYear = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                   "November", "December"]

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


def validate_day(d):
    try:
        d = int(d)
    except:
        raise ValueError("day should be an int")
    if d < 1 or d > 31:
        raise ValueError("Sorry, day should only be in  [1, 31]")


def extract_type(section):
    return config.get(section, 'Type')


def extract_message(section):
    return config.get(section, 'Message')


def extract_days(section):
    return config.get(section, 'Day')


def extract_months(section):
    return config.get(section, 'Month')


def extract_weekdays(section):
    return config.get(section, 'Weekday')


for i in config.sections():

    taskType = extract_type(i)
    validate_task_type(taskType)

    if taskType == 'daily':
        message = extract_message(i)
        logging.info("Everything is OK! :D I'll remember you \"{}\" every day ".format(message))
        sendMail.sendNotification(i, message)

    if taskType == 'weekly':
        for j in extract_weekdays(i).split(','):
            validate_weekday(j)
            if daysOfTheWeek.index(j) == now.weekday():
                message = extract_message(i)
                logging.info("Everything is OK! :D I'll remember you \"{}\" every day ".format(message))
                sendMail.sendNotification(i, message)

    if taskType == 'monthly':
        for j in extract_days(i).split(','):
            validate_day(j)
            if day == j:
                message = extract_message(i)
                logging.info("Everything is OK! :D I'll remember you \"{}\" every {} of the month ".format(message, j))
                sendMail.sendNotification(i, message)

    if taskType == 'yearly':
        m = extract_months(i)
        d = extract_days(i)
        if len(m.split(',')) > 1 or len(d.split(',')) > 1:
            raise ValueError("Sorry, yearly task should only contain one specific date")
        validate_day(d)
        validate_month(m)
        if d == day and monthsOfTheYear.index(m) + 1 == int(month):
            message = extract_message(i)
            logging.info(
                "Everything is OK! :D I'll remember you \"{}\" every year, the {} of the month {}".format(message, day,
                                                                                                          month))
            sendMail.sendNotification(i, message)

    if taskType == 'free':
        for j in extract_months(i).split(','):
            validate_month(j)
            if monthsOfTheYear.index(j) + 1 == int(month):
                for k in extract_days(i).split(','):
                    validate_day(k)
                    if day == k:
                        message = extract_message(i)
                        logging.info(
                            "Everything is OK! :D I'll remember you \"{}\" every {} of the months {}".format(message,
                                                                                                             day,
                                                                                                             month))
                        sendMail.sendNotification(i, message)
