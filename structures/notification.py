class Notification(object):
	''' represents a notification that should be broadcast due to an interesting development in the market '''

	def __init__(self, index, date, close, notification, strategy):
		self.index = index
		self.notification = notification
		self.strategy = strategy
		self.date = date
		self.close = close