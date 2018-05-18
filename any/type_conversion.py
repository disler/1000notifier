import datetime
import time

def longToDate(longDate, easyRead = False):
	''' converts dates as type long to dates '''

	date = datetime.datetime.fromtimestamp(longDate / 1e3)

	if easyRead:
		return date.strftime("%d %B %Y %I:%M:%S %p")

	return date

def dateToLong(dtDate):
	''' converts date into long with ms '''

	return long(time.mktime(dtDate.timetuple()) * 1e3 + dtDate.microsecond / 1e3)