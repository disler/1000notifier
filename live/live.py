
from strategy import strategy
from any import date_helpers
from transforms import transforms
import constants
import time
import network.api
from any.type_conversion import dateToLong
from datetime import datetime

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
		singlePeriodWaitTime = self.get_single_period_wait_time(self.lookback, self.period)

		# initial data fetch
		rawCandles = network.api.candles(self.pair, self.period, dtStart, dtEnd)

		# transform data
		transformed = transforms.candles_single_array_to_type_array(rawCandles)

		# add our current data set to our uniquely seen open times
		self.add_to_unique_candles(transformed['date'])

		# the point on our list of transformed candles we've already run strategy up to
		candleIterationIndex = 0

		# infinite loop
		while True:

			# fetch the previous n candles (ideally just 1)
			newCandles = network.api.candles(self.pair, self.period, None, None, constants.LIVE_CANDLE_LOOP_BACKTRACK)

			# filter out candles we already have
			newCandles = [_candle for _candle in newCandles if _candle[0] not in self.uniqueCandlesViaOpenTime]

			# if we have new candles to add
			if len(newCandles) > 0:
				# transform the new candles, starting at index == length of our current transformed list
				newCandlesTransformed = transforms.add_many_candles_to_transformed(transformed, newCandles, len(transformed))

			# while we haven't caught up to the end of the transformed list run our strategy
			while candleIterationIndex < len(transformed):

				# run strategy
				transformed = self.strategy.strategy(transformed, candleIterationIndex)

				# increment index
				candleIterationIndex += 1

			# should notify
			shouldNotify = False

			# if new notification pass it to our funcNotifier with the data to create chart and notify however it sees fit
			for _clsNotification in transformed['notification']:
				if _clsNotification.isNew():
					shouldNotify = True
					break

			# if we are marked to notify
			if shouldNotify:

				# fire notifier
				self.funcNotifier(transformed)

				# set the notification status as seen
				for _clsNotification in transformed['notification']:
					_clsNotification.observed()
			
			# delay for the next candle to come into existance
			time.sleep(singlePeriodWaitTime)
		pass

	def add_to_unique_candles(self, lstOpenTime):
		''' @MUTATES given a list of open times add them to our uniquely seen candle list '''

		for _openTime in lstOpenTime:
			if isinstance(_openTime, datetime):
				self.uniqueCandlesViaOpenTime.add(dateToLong(_openTime)
			else:
				# must be long here
				assert isinstance(_openTime, long)
				self.uniqueCandlesViaOpenTime.add(_openTime)

	def get_single_period_wait_time(self, lookback, period):
		''' obtain the amount of time to sleep before querying again '''

		# 1m -> 1, 'minutes', 15m -> 15, 'minutes', 1h -> 1, 'hours'
		periodAmount, periodType = constants.CANDLE_STICK_INTERVAL_TO_TIME_TUPLE[period]

		# convert one unit down (at least)
		waitTimeInSeconds = 0

		if periodType == 'minutes':
			waitTimeInSeconds = periodAmount * 60
		elif periodType == 'hours':
			waitTimeInSeconds = periodAmount * 60 * 60
		elif periodType == 'days':
			waitTimeInSeconds = periodAmount * 60 * 60 * 24
		elif periodType == 'weeks':
			raise Exception('period type weeks not calc"d')

		# add some padding because time
		waitTimeInSeconds += constants.WAIT_TIME_LOOP_PADDING

		return waitTimeInSeconds


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