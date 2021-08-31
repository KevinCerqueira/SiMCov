import time
from random import randint

class Oximeter:
	
	signals = [-1, 1]
	
	saturation = 0
	init_value = 0
	
	def __init__(self):
		print('initializing...')
		time.sleep(randint(4,6))
		self.init_value = randint(90, 99)
	
	def work(self):
		self.saturation = self.sortValue(self.init_value)
		# print('{}%'.format(self.saturation))
		time.sleep(3)
		
	def sortValue(self, current_value):
		return current_value + (randint(0, 1) * self.sortSignal()) 
	
	def sortSignal(self):
		return self.signals[randint(0, 1)]
		
# if __name__ == '__main__':
# 	oximeter = Oximeter()
# 	oximeter.work()