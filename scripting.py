import inspect
import sys
class DefTest():
	def test(self):
		return 'WOW!'

def getClasses():
	clsmembers = inspect.getmembers(__import__(__name__), inspect.isclass)
	return clsmembers

print getClasses()