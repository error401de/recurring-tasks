import configparser, os, shutil, time

def createBackup():
    path = os.path.dirname(os.path.abspath(__file__)) # path to this .py file

    config = configparser.ConfigParser()
    config.read(path + '/config.ini')
    retentionLevel = int(config.get("backup", "Retention"))

    createBackupFile(path)
    clearOldestFiles(retentionLevel, path)

def createBackupFile(path):
    currentTime = str(int(time.time())) # gets time since epoch
    filePath = path + "/backup/tasks.ini.backup." + currentTime
    shutil.copyfile(path + "/tasks.ini", filePath)  

def clearOldestFiles(retentionLevel, path):
    backupFiles = [path + "/backup/" + x for x in os.listdir(path + "/backup") if isBackup(x)]

    numFilesToDelete = len(backupFiles) - retentionLevel
    if numFilesToDelete < 1:
        return

    backupFiles = sorted(backupFiles) # sort files alphanumerically, so old files are first
    for i in range(numFilesToDelete):
        os.remove(backupFiles[i])

def isBackup(fileName):
    return fileName.startswith("tasks.ini.backup.")
