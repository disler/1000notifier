import inspect
import strategy
from logger.logger import log

def backtest(oData, sStrategy, strategyArgs={}):
	'''
		Given candles and a strategy - backtest by creating notifications based on 'setups' that the strategy conveys - add to data
	'''

	# create an instance of the strategy that we want 
	instStrategy = strategy.create_strategy_instance(sStrategy, strategyArgs)

	for _index in oData['index']:
		oData = instStrategy.strategy(oData, _index)

	return oData