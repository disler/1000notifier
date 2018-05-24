'''
	Creates simple charts
'''

import plotly
import plotly.graph_objs as go

from datetime import datetime
from logger.logger import log

def add_to_trace_if_exist(oData, indicator):
	''' return a list to be combined with previous traes -> append traces given the indicator exists '''

	if indicator not in oData:
		log("indicator {} not in oData keys: {}".format(indicator, oData.keys()))
		return []

	oTrace = {}

	# Simple moving average
	if indicator == 'SMA':
		if type(list(oData[indicator])) == list:
			oTrace = dict(
				type="scatter",
				x=oData['date'],
				y=oData[indicator],
				mode="lines",
				line = dict( width = 1 ),
				marker = dict( color = '#E377C2' ),
				yaxis = 'y2',
				name='Moving Average' 
			)

	# exponential moving average 10
	elif indicator == 'EMA_10':
		if type(list(oData[indicator])):
			oTrace = dict(
				type="scatter",
				x=oData['date'],
				y=oData[indicator],
				mode="lines",
				line = dict( width = 2 ),
				marker = dict( color = '#d18f4d' ),
				yaxis = 'y2',
				name='Exponential Moving Average (10)' 
			)

	# exponential moving average 21
	elif indicator == 'EMA_21':
		if type(list(oData[indicator])):
			oTrace = dict(
				type="scatter",
				x=oData['date'],
				y=oData[indicator],
				mode="lines",
				line = dict( width = 2 ),
				marker = dict( color = '#72d1d8' ),
				yaxis = 'y2',
				name='Exponential Moving Average (21)' 
			)

	return [oTrace]



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
	volume = oData.get('volume', False)
	index = oData.get('index', False)
	sma = oData.get('SMA', False)
	up_or_down = oData.get('up_or_down')
	colors = ["#aFa" if _step == 'up' else "#Faa" for _step in up_or_down]

	assert date and len(date) > 0, "Required field oData[date] is missing"
	assert open and len(open) > 0, "Required field oData[open] is missing"
	assert high and len(high) > 0, "Required field oData[high] is missing"
	assert low and len(low) > 0, "Required field oData[low] is missing"
	assert close and len(close) > 0, "Required field oData[close] is missing"
	assert index and len(index) > 0, "Required field oData[index] is missing"
	assert volume and len(volume) > 0, "Required field oData[volume] is missing"
	assert up_or_down and len(up_or_down) > 0, "Required field oData[up_or_down] is missing"

	# fill with traces
	data = []

	# config settings
	layout = dict()

	oCandleData = dict(
		type = 'candlestick',
		open = open,
		high = high,
		low = low,
		close = close,
		x = date,
		yaxis = 'y2',
		name = 'candles',
		increasing = dict( line = dict( color = "#aFa" ) ),
		decreasing = dict( line = dict( color = "#Faa" ) ),
	)	
	
	oVolumeData = dict(
		type="bar",
		yaxis="y",
		name="Volume",
		marker = dict( color = colors ),
		x=date,
		y=volume,
	)

	data = data + add_to_trace_if_exist(oData, 'SMA')
	data = data + add_to_trace_if_exist(oData, 'EMA_' + str(10))
	data = data + add_to_trace_if_exist(oData, 'EMA_' + str(21))
	
	data.append(oCandleData)
	data.append(oVolumeData)

	layout['plot_bgcolor'] = 'rgb(0, 0, 0)'
	layout['xaxis'] = dict( rangeselector = dict( visible = True ) )
	layout['yaxis'] = dict( domain = [0, 0.2], showticklabels = True )
	layout['yaxis2'] = dict( domain = [0.2, 1] )
	#layout['legend'] = dict( orientation = 'h', y=0.9, x=0.3, yanchor='bottom' )
	#layout['margin'] = dict( t=40, b=40, r=40, l=40 )

	figure = dict(data=data, layout=layout)


	plotly.offline.plot(figure, filename='simple_candlestick.html')



'''
	trace = go.Candlestick(
		x=date,
		open=open,
		high=high,
		low=low,
		close=close,
		y=volume
	)

	data = [trace]

	plotly.offline.plot(data, filename='simple_candlestick')
'''