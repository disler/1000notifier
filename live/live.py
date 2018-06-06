
from strategy import strategy
from any import date_helpers
import constants


class LiveNotifier(object):
	''' periodically queries api and runs strategy on fetched data, if a strategy finds a match a notification function is called '''
	
	def __init__(self, pair, period, strategyName, strategyArgs, lookback = 50):
		''' 
			setup required defaults 
			pair - trading pair
			period - candles period to observe
			strategyName - prebuild strategy to run
			lookback - number of candles to query and take account into consistently
		'''

		# our trading pair
		self.pair = pair

		# period (1m, 5m, 15m, etc)
		self.period = period

		# our strategy name
		self.strategyName = strategyName

		# strategy args
		self.strategyArgs = strategyArgs

		# strategy object
		self.strategy = None

		# our look bac time
		self.lookback = lookback

		# we only want to be holding onto <lookback> number of candles at any time - stay fast and up to date
		self.CANDLE_LIMIT = lookback

		# notifier function dynamically passed in
		self.funcNotifier = None

		# our list of rolling candle streams within a 'lookback' of 50.
		self.candleStream = []

		# list of opening times which uniquely identify each candle stream - this is so we know what candles have been seen already when querying
		self.uniqueCandlesViaOpenTime = set()

	def run(self):
		''' begin the notifier '''

		# mount the strategy
		self.strategy = strategy.create_strategy_instance(self.strategyName, self.strategyArgs)

		# get start, end date based on lookback and period
		dtStart, dtEnd = self.get_start_and_end_datetime(self.lookback, self.period)

		# get our wait time (1 period plus a little)
		singlePeriodWaitTime = get_single_period_wait_time(self.lookback, self.period)
		
		pass

	def get_single_period_wait_time(self, lookback, period):
		''' obtain the amount of time to sleep before querying again '''
		return 1000

	def get_start_and_end_datetime(self, lookback, period):
		''' based on our lookback and period, determine our datetime start and datetime end '''

		# 1m -> 1, 'minutes', 15m -> 15, 'minutes', 1h -> 1, 'hours'
		periodAmount, periodType = constants.CANDLE_STICK_INTERVAL_TO_TIME_TUPLE[period]

		# multiply our period amount times how many candles we want to look back to get our date start
		lookbackWithPeriod = periodAmount * lookback

		# get our date start and end
		dtStart, dtEnd = date_helpers.date_range(periodType, lookbackWithPeriod)

		return (dtStart, dtEnd)


	def set_notifier(self, funcNotifier):
		''' set the notifier '''
		self.funcNotifier = funcNotifier