"""
	Makes api calls directly to binance
"""

import client
import constants
import datetime
import any.type_conversion as type_conversion

def successfulAPIResponse(clsResponse):
	'''
		returns true of response object was successful
	'''
	return clsResponse.status_code == 200

def test_connectivity():
	"""
		:return boolean: if connection was made
	"""

	clsResponse = client.api_call_sync(constants.API_BINANCE_PING)

	if not successfulAPIResponse(clsResponse):
		return

	return clsResponse.json() == {}

def check_server_time():
	"""
		return server time as datetime
	"""
	clsResponse = client.api_call_sync(constants.API_BINANCE_TIME)

	if not successfulAPIResponse(clsResponse):
		return

	iServerTime = clsResponse.json().get('serverTime')

	dtServerTime = type_conversion.longToDate(iServerTime)

	return dtServerTime

def exchange_information():
	'''
		returns trading rules and symbol information
	'''

	clsResponse = client.api_call_sync(constants.API_BINANCE_EXCHANGE_INFO)

	if not successfulAPIResponse(clsResponse):
		return

	return clsResponse.json()

def order_book(symbol, limit = 100):
	"""
		returns up to <limit> orders for currency <symbol>

		symbol:string - required - market data for a trading pair
		limit:int - Default 100; max 1000. Valid limits:[5, 10, 20, 50, 100, 500, 1000]
	"""

	assert symbol, "order_book() requires <symbol> param"
	assert limit in [5, 10, 20, 50, 100, 500, 1000], "order_book requires <limit> to be in [5, 10, 20, 50, 100, 500, 1000]"

	oParams = {
		"symbol": symbol,
		"limit": limit
	}

	clsResponse = client.api_call_sync(constants.API_BINANCE_ORDER_BOOK, oParams)

	return clsResponse.json()

def recent_trades(symbol, limit = 500):
	'''
		returns up to <limit> recent trades for <symbol>
	'''

	assert symbol, "recent_trades() requires <symbol> param"
	assert limit <= 500, "limit cannot be greater than 500"
	
	oParams = {
		"symbol": symbol,
		"limit": limit
	}

	clsResponse = client.api_call_sync(constants.API_BINANCE_RECENT_TRADES, oParams)

	return clsResponse.json()

def candles(symbol, interval, startTime = None, endTime = None, limit = 500):
	'''
		returns candles in two ways
			1. if startTime and endTime are not set the mist recent <limit> candles are sent
			2. if startTime and endTime are sent returns candles inbetween that time

		startTime and endTime must be converted into timestamps with milliseconds
	'''

	assert symbol, "candles() requires <symbol> param"
	assert interval in constants.CANDLE_STICK_INTERVALS, ("candles() requires <interval> param to be in {}".format(constants.CANDLE_STICK_INTERVALS))

	# no time range -> return the <limit> most previous candles for <symbol>
	if startTime == None or endTime == None:

		assert limit <= 500, "candles() requires <limit> to be less than 500"

		oParams = {
			"symbol": symbol,
			"interval": interval,
			"limit": limit
		}
	# use the datetime range -> return <?> candles between <startTime> and <endTime> for <symbol>
	else:

		assert startTime < endTime, "candles() <startTime> param must be less than <endTime>"

		startTime = type_conversion.dateToLong(startTime)
		endTime = type_conversion.dateToLong(endTime)

		oParams = {
			"symbol": symbol,
			"interval": interval,
			"startTime": startTime,
			"endTime": endTime
		}

	clsResponse = client.api_call_sync(constants.API_BINANCE_CANDLESTICK, oParams)

	return clsResponse.json()