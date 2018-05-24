"""
	Converts data from one format to another
"""

from logger.logger import log
import any.type_conversion as type_conversion

def candles_single_array_to_type_array(candles):
	"""
		takes candles from the api.candles request and creates 5 arrays by name into a dict

		[
			[
				1499040000000,      // Open time
				"0.01634790",       // Open
				"0.80000000",       // High
				"0.01575800",       // Low
				"0.01577100",       // Close
				"148976.11427815",  // Volume
				1499644799999,      // Close time
				"2434.19055334",    // Quote asset volume
				308,                // Number of trades
				"1756.87402397",    // Taker buy base asset volume
				"28.46694368",      // Taker buy quote asset volume
				"17928899.62484339" // Ignore
			],
			...
		] 
		CONVERTED INTO
		{
			date = [<date time>, ...],
			open = [int, ...]
			high = [int, ...]
			low = [int, ...]
			close = [int, ...]
			volume = [int, ...]
		}
	"""

	if not candles or len(candles) == 0:
		log('no candles to transform returning None')
		return None

	log("running 'candles_single_array_to_type_array()' on candles -> {}".format(candles))

	lstDate = []
	lstOpen = []
	lstHigh = []
	lstLow = []
	lstClose = []
	lstVolume = []
	lstIndex = []
	lstUpOrDown = []

	for _index, _lstCandle in enumerate(candles):

		_dtOpen = type_conversion.longToDate(_lstCandle[0])
		_open = float(_lstCandle[1])
		_high = float(_lstCandle[2])
		_low = float(_lstCandle[3])
		_close = float(_lstCandle[4])
		_volume = float(_lstCandle[5])

		lstDate.append(_dtOpen)
		lstOpen.append(_open)
		lstHigh.append(_high)
		lstLow.append(_low)
		lstClose.append(_close)
		lstVolume.append(_volume)
		lstIndex.append(_index)

	# calculate increased/stay/decreased
	for _index in lstIndex:
		_close = lstClose[_index]
		_open = lstOpen[_index]
		if _close > _open:
			lstUpOrDown.append("up")
		elif _close == _open:
			lstUpOrDown.append("steady")
		else:
			lstUpOrDown.append("down")

	oTransformed = {
		"date": lstDate,
		"open": lstOpen,
		"high": lstHigh,
		"low": lstLow,
		"close": lstClose,
		"volume": lstVolume,
		"index": lstIndex,
		'up_or_down': lstUpOrDown
	}

	log("completed data transform -> {}".format(oTransformed))

	return oTransformed