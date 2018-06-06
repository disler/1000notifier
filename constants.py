API_BINANCE_ROOT = "https://api.binance.com"
API_BINANCE_PING = API_BINANCE_ROOT + "/api/v1/ping"
API_BINANCE_TIME = API_BINANCE_ROOT + "/api/v1/time"
API_BINANCE_EXCHANGE_INFO = API_BINANCE_ROOT + "/api/v1/exchangeInfo"
API_BINANCE_ORDER_BOOK = API_BINANCE_ROOT + "/api/v1/depth"
API_BINANCE_RECENT_TRADES = API_BINANCE_ROOT + "/api/v1/trades"
API_BINANCE_CANDLESTICK = API_BINANCE_ROOT + "/api/v1/klines"
LOG_FILE_PATH = "./feedback/"
CANDLE_STICK_INTERVALS = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]
DATE_DELTA_TYPES = ["minutes", "hours", "days", "weeks", "months"]
POSITIVE_COLOR = "#aFa"
NEGATIVE_COLOR ="#Faa"
STRATEGY_VOLUME_CHANGE = "volume_change"
CANDLE_STICK_INTERVAL_TO_TIME_TUPLE = {
	"1m": (1, 'minutes'),
	"3m": (3, 'minutes'),
	"5m": (5, 'minutes'),
	"15m": (15, 'minutes'),
	"30m": (30, 'minutes'),
	"1h": (1, 'hours'),
	"2h": (2, 'hours'),
	"4h": (4, 'hours'),
	"6h": (6, 'hours'),
	"8h": (8, 'hours'),
	"12h": (12, 'hours'),
	"1d": (1, 'days'),
	"3d": (3, 'days'),
	"1w": (1, 'weeks'),
	"1M": (4.34524, 'weeks'),
}