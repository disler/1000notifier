class Notification(object):
	''' represents a notification that should be broadcast due to an interesting development in the market '''

	def __init__(self, index, date, close, notification, strategy):
		self.index = index
		self.notification = notification
		self.strategy = strategy
		self.date = date
		self.close = close

		# if this notification has been emitted
		self.hasBeenBroadcasted = False

	def isNew(self):
		''' if this is a new notification that has need been seen '''
		return self.hasBeenBroadcasted == False

	def observed(self):
		''' this notification has been awknowledged '''
		self.hasBeenBraodcasted = True