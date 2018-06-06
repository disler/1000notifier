'''
	Contains strategies for predicting market shifts
'''
from structures.notification import Notification
from logger.logger import log
import constants
import inspect

def create_strategy_instance(strategy, strategyArgs):
	''' generates a strategy '''

	# get our strategy
	lstStrategies = inspect.getmembers(__import__(__name__), predicate=inspect.isclass)
	print lstStrategies
	oMapStrategyNameToStrategyClass = {_tuple[0]:_tuple[1] for _tuple in lstStrategies if "Strategy" in _tuple[0]}
	clsStrategy = oMapStrategyNameToStrategyClass.get(strategy, False)

	# existance check
	if clsStrategy == False:
		error = 'strategy {} does not exist available options are {}'.format(strategy, oMapStrategyNameToStrategyClass)
		log(error)
		raise Exception(error)

	instStrategy = clsStrategy()
	instStrategy.setArgs(strategyArgs)

	return instStrategy

class StrategyVolumeChange(object):
	'''
		when volume increases or decreases based on a multiplier create a notification
	'''

	def setArgs(self, strategyArgs):

		log("setting StrategyVolumeChange() args -> {}".format(strategyArgs))
		
		self.strategyArgs = strategyArgs

	def strategy(self, oData, index):

		if index == 0:
			pass
		else:
			# get our volume change threshold in which we'd create a notification
			increaseRatio = self.strategyArgs.get('increase_ratio', 2)
			decreaseRatio = self.strategyArgs.get('decreased_ratio', 2)

			# get volume
			previousVolume = oData['volume'][index-1]
			currentVolume = oData['volume'][index]

			# get volume direction
			currentUpOrDown = oData['up_or_down'][index]
			previousUpOrDown = oData['up_or_down'][index-1]

			#increase ratio amount
			previousVolumeAndIncreaseRatio = previousVolume * increaseRatio
			previousVolumeAndDecreasedRatio = previousVolume * decreaseRatio
			
			# log
			log("STRATEGY: running volume_change strategy with index: {}, previousVolume: {}, currentVolume: {}, currentUpOrDown: {}, previousUpOrDown: {}, previousVolumeAndIncreaseRatio: {}".format(index, previousVolume,currentVolume,currentUpOrDown,previousUpOrDown,previousVolumeAndIncreaseRatio))

			if currentUpOrDown == 'up' and previousUpOrDown == 'up':
				if currentVolume > previousVolumeAndIncreaseRatio:

					log("STRATEGY: volume_change found notifiable case at index {}".format(index))

					date = oData['date'][index]
					close = oData['close'][index]

					notificationMessage = 'UPWARD_VOLUME_CHANGE: {} -> {} (> {} x previous volume)'.format(previousVolume, currentVolume, increaseRatio)
					notification = Notification(index, date, close, notificationMessage, constants.STRATEGY_VOLUME_CHANGE)
					oData['notification'].append(notification)

			if currentUpOrDown == 'down' and previousUpOrDown == 'down':
				if currentVolume > previousVolumeAndDecreasedRatio:

					log("STRATEGY: volume_change found notifiable case at index {}".format(index))

					date = oData['date'][index]
					close = oData['close'][index]

					notificationMessage = 'DOWNWARD_VOLUME_CHANGE: {} -> {} (> {} x previous volume)'.format(previousVolume, currentVolume, increaseRatio)
					notification = Notification(index, date, close, notificationMessage, constants.STRATEGY_VOLUME_CHANGE)
					oData['notification'].append(notification)
 
		return oData