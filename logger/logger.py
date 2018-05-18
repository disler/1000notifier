import os
import constants

def formatMessage(message):
	return "\n\n{}".format(message)

def log(message):
	
	sFilePath = constants.LOG_FILE_PATH + "/log.txt"

	sFormattedMessage = formatMessage(message)
	
	with open(sFilePath, "a") as fFile:
		fFile.write(sFormattedMessage)
		fFile.close()