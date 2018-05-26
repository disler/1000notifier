import inspect
import sys
from strategy
class DefTest():
	def test(self):
		return 'WOW!'

def getClasses():
	clsmembers = inspect.getmembers(strategy, inspect.isclass)
	return clsmembers

print getClasses()