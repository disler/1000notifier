'''
	Creates simple charts
'''

import plotly
import plotly.graph_objs as go
from any.data_conversion import up_down_to_colors
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

def simple_volume_bar(oData):
	'''
		create a simple bar chart

		requires oData to be {
			date:dt[]|str[],
			volume:int[]
		}
	'''
	date = oData.get('date', False)
	volume = oData.get('volume', False)
	colors = up_down_to_colors(oData.get('up_or_down'))

	assert date and len(date) > 0, "Required field oData[date] is missing"
	assert volume and len(volume) > 0, "Required field oData[volume] is missing"
	assert colors and len(colors) > 0, "Required field oData[up_or_down] is missing"

	traces = []
	layout = {}

	oVolumeData = dict(
		type="bar",
		x=date,
		y=volume,
		marker = dict( color = colors ),
		yaxis="y"
	)

	traces.append(oVolumeData)

	chart = dict(data=traces, layout=layout)

	plotly.offline.plot(chart, filename="simple_volume_bar.html")

def build_annotations_from_notifications(notifications):
	''' from a list of structures:notification:Notifications() create an annotation to display the event of importance '''
	
	annotations = []

	for _notification in notifications:
		
		annotation = dict(
            x=_notification.date,
            y=_notification.close,
            yref='y2',
            text=_notification.strategy,
			hovertext=_notification.notification
            #showarrow=True,
            #arrowhead=7,
            #ax=0,
            #ay=-40
        )

		annotations.append(annotation)

	return annotations

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
	colors = up_down_to_colors(up_or_down) 
	notifications = oData.get('notification', [])

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

	notification_annotations = build_annotations_from_notifications(notifications)

	log("notification_annotations: {}".format(notification_annotations))
	
	data.append(oCandleData)
	data.append(oVolumeData)

	layout['title'] = oData.get('title', 'Default Title')
	layout['annotations'] = notification_annotations
	layout['xaxis'] = dict( rangeselector = dict( visible = True ) )
	layout['yaxis'] = dict( domain = [0, 0.4], showticklabels = True )
	layout['yaxis2'] = dict( domain = [0.4, 1] )
	#layout['plot_bgcolor'] = 'rgb(0, 0, 0)'
	#layout['legend'] = dict( orientation = 'h', y=0.9, x=0.3, yanchor='bottom' )
	#layout['margin'] = dict( t=40, b=40, r=40, l=40 )

	figure = dict(data=data, layout=layout)


	plotly.offline.plot(figure, filename=oData.get('file_name', 'default_file_name.html'))



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