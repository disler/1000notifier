import constants as constants
import network.api
import pprint
from any.type_conversion import longToDate as dt, dateToLong as dtl
import datetime
import transforms.transforms as transforms
import charting.simple_chart as charting
import talib


dtStart = datetime.datetime.now() - datetime.timedelta(days=1)
dtEnd = datetime.datetime.now() - datetime.timedelta()

response = network.api.candles("ZRXBTC", "15m", dtStart, dtEnd)
print pprint.pformat(response)

transformed = transforms.candles_single_array_to_type_array(response)
print pprint.pformat(transformed)

charting.simple_candle(transformed)