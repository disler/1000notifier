'''
	Creates simple charts
'''

import plotly
import plotly.graph_objs as go

from datetime import datetime


def simple_candle(oData):
	'''
		creates a simple candle chart

		requires oData to be {
			date:str[]
			open:int[]
			high:int[]
			low:int[]
			close:int[]
		}
	'''

	# pull fields
	date = oData.get('date', False)
	open = oData.get('open', False)
	high = oData.get('high', False)
	low = oData.get('low', False)
	close = oData.get('close', False)

	assert date and len(date) > 0, "Required field oData[date] is missing"
	assert open and len(open) > 0, "Required field oData[open] is missing"
	assert high and len(high) > 0, "Required field oData[high] is missing"
	assert low and len(low) > 0, "Required field oData[low] is missing"
	assert close and len(close) > 0, "Required field oData[close] is missing"


	trace = go.Candlestick(
		x=date,
		open=open,
		high=high,
		low=low,
		close=close,
	)

	data = [trace]

	plotly.offline.plot(data, filename='simple_candlestick')