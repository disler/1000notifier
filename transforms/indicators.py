import talib
import numpy as np

def safeNumpyGet(oData, key):
	''' performs a safe list -> numpylist conversion '''
	
	lstKey = oData.get(key, False)

	assert lstKey and len(lstKey) > 0, 'Missing {} for sma'.format(key)

	return np.asarray(lstKey)

def sma(oData, period):
	''' attach the sma '''

	oData['SMA'] = talib.SMA(safeNumpyGet(oData, 'close'), period)

	return oData

def ema(oData, period):
	''' attach the ema '''
	
	oData['EMA_'+str(period)] = talib.EMA(safeNumpyGet(oData, 'close'), period)

	return oData
