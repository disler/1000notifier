import constants as constants
import network.api
import pprint
from any.type_conversion import longToDate as dt, dateToLong as dtl
import datetime
from transforms import transforms, indicators
import charting.simple_chart as charting
from any.date_helpers import date_range


dtStart, dtEnd = date_range("days", 2, None, None)

response = network.api.candles("ZRXBTC", "30m", dtStart, dtEnd)

transformed = transforms.candles_single_array_to_type_array(response)

transformed = indicators.ema(transformed, 10)
transformed = indicators.ema(transformed, 21)

charting.simple_candle(transformed)