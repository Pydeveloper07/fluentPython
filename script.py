import datetime

with open('/Users/blacktiger/dateInfo.txt', 'a') as outFile:
    outFile.write('\n' + str(datetime.datetime.now()))
