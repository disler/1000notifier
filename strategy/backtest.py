import inspect
import strategy
from logger.logger import log

def backtest(oData, sStrategy, strategyArgs={}):
	'''
		Given candles and a strategy - backtest by creating notifications based on 'setups' that the strategy conveys - add to data
	'''

	# get our strategy
	lstStrategies = inspect.getmembers(strategy, predicate=inspect.isclass)
	print lstStrategies
	oMapStrategyNameToStrategyClass = {_tuple[0]:_tuple[1] for _tuple in lstStrategies if "Strategy" in _tuple[0]}
	clsStrategy = oMapStrategyNameToStrategyClass.get(sStrategy, False)

	# existance check
	if clsStrategy == False:
		error = 'strategy {} does not exist available options are {}'.format(sStrategy, oMapStrategyNameToStrategyClass)
		log(error)
		raise Exception(error)

	# create a new location for strategy reports/notification
	oData['notification'] = []

	instStrategy = clsStrategy()
	instStrategy.setArgs(strategyArgs)

	for _index in oData['index']:
		oData = instStrategy.strategy(oData, _index)

	return oData