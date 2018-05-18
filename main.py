import constants as constants
import network.api
import pprint
from any.type_conversion import longToDate as dt, dateToLong as dtl
import datetime

dtStart = datetime.datetime.now() - datetime.timedelta(hours=2)
dtEnd = datetime.datetime.now() - datetime.timedelta()

response = network.api.candles("ZRXBTC", "15m", dtStart, dtEnd)
print pprint.pformat(response)