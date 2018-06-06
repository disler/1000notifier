from any.date_helpers import date_range
from any.data_conversion import generate_title
from transforms import transforms, indicators, generic
from any.type_conversion import longToDate as dt, dateToLong as dtl
from logger.logger import log
from strategy import backtest
import pprint
import datetime
import network.api
import constants as constants
import charting.simple_chart as charting

from live import live


notifier = live.LiveNotifier('ZRXBTC', '1m', "StrategyVolumeChange", {"increase_ratio": 1.5})








def backtest_test():
	# base variables
	pair = "ZRXBTC"
	period = "15m"
	dtStart, dtEnd = date_range("days", 2, None, None)

	# query for candles
	response = network.api.candles(pair, period, dtStart, dtEnd)

	transformed = transforms.candles_single_array_to_type_array(response)


	title = generate_title(pair, period, dtStart, dtEnd)
	transformed = generic.set(transformed, 'title', title)
	transformed = generic.set(transformed, 'file_name', 'simple_chart.html')

	backtested = backtest.backtest(transformed, 'StrategyVolumeChange', {'increase_ratio': 2.0})

	charting.simple_candle(backtested)



def chart_tests():
	# base variables
	pair = "ZRXBTC"
	period = "15m"
	dtStart, dtEnd = date_range("days", 2, None, None)

	# query for candles
	response = network.api.candles(pair, period, dtStart, dtEnd)

	transformed = transforms.candles_single_array_to_type_array(response)

	title = generate_title(pair, period, dtStart, dtEnd)

	# convert data and setup additional params
	transformed = generic.set(transformed, 'title', title)
	transformed = generic.set(transformed, 'file_name', 'simple_chart.html')
	#transformed = indicators.ema(transformed, 10)
	#transformed = indicators.ema(transformed, 21)

	charting.simple_candle(transformed)
	#charting.simple_volume_bar(transformed)