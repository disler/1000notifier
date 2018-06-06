import constants
import datetime

def date_range(startType, startAmount, endType=None, endAmount=None):
	''' returns a 2-tuple dtStart and dtEnd for time ranges. Time delta takes, 'days', 'seconds', 'minutes', 'hours', 'weeks' '''

	assert startType in constants.DATE_DELTA_TYPES, "startType {} is invalid".format(startType)

	dtStart = datetime.datetime.now() - datetime.timedelta(**{startType: startAmount})
	
	if endType == None or endAmount == None:
		dtEnd = datetime.datetime.now()
	else:
		dtEnd = datetime.datetime.now() - datetime.timedelta(**{endType: endAmount})

	return dtStart, dtEnd
	