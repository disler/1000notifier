import constants
from logger.logger import log

def up_down_to_colors(lstUpOrDown):
	''' converts a list of ['up', 'down', 'steady'] -> [<upcolor>. <downcolor> <steady>] '''

	# just a quick logging check should probably remove htis
	for _element in lstUpOrDown:
		if _element not in ['up', 'down', 'steady']:
			log('when converting up or down to colors found invalid value {}'.format(_element))

	return [constants.POSITIVE_COLOR if _step == 'up' else constants.NEGATIVE_COLOR for _step in lstUpOrDown]

def generate_title(sPair, sPeriod, dtStart, dtEnd):
	''' based on the pair, period, start, and end time generate a good title that gives information '''

	sStart = dtStart.strftime("%Y-%m-%d %H:%M:%S")
	sEnd = dtEnd.strftime("%Y-%m-%d %H:%M:%S")

	return "{} ({})<br>{} - {}".format(sPair, sPeriod, sStart, sEnd)