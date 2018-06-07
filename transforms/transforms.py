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
		upOrDown = _determine_up_or_down(_open, _close)
		lstUpOrDown.append(upOrDown)

	oTransformed = {
		"date": lstDate,
		"open": lstOpen,
		"high": lstHigh,
		"low": lstLow,
		"close": lstClose,
		"volume": lstVolume,
		"index": lstIndex,
		'up_or_down': lstUpOrDown

		# notification list starts empty
		'notification': []
	}

	log("completed data transform -> {}".format(oTransformed))

	return oTransformed

def add_many_candles_to_transformed(transformed, candles, startingIndex):
	''' converts several candles into the transformemd list '''

	# run candle transform for each candle
	for index, _candle in enumerate(candles):
		transformed = add_candle_to_transformed(transformed, _candle, index + startingIndex)

	return transformed

def add_candle_to_transformed(transformed, candle, index):
	''' convert a single candle into the transformed list '''

	log('adding candle: {}, at index: {}, to data: \n\n{}\n\n'.format(candle, index, transformed))

	_dtOpen = type_conversion.longToDate(candle[0])
	_open = float(candle[1])
	_high = float(candle[2])
	_low = float(candle[3])
	_close = float(candle[4])
	_volume = float(candle[5])

	transformed['date'].append(_dtOpen)
	transformed['open'].append(_open)
	transformed['high'].append(_high)
	transformed['low'].append(_low)
	transformed['close'].append(_close)
	transformed['volume'].append(_volume)
	transformed['index'].append(index)

	return transformed




''' "private" helpers '''

def _determine_up_or_down(open, close):
	if close > open:
		return "up"
	elif close == open:
		return "steady"
	else:
		return "down"