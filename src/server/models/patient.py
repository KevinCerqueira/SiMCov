from oximeter import Oximeter
import threading

class Patient:
	
	patientSaturation = 0
	
	def measureSaturation(self):
		saturation = Oximeter()
		while(1):
			saturation.work()
			self.patientSaturation = saturation.saturation
			print('{}%'.format(self.patientSaturation))
	
	def startMeasureSaturation(self):
		threading.Thread(target=self.measureSaturation()).start()

if __name__ == '__main__':
	patient = Patient()
	patient.startMeasureSaturation()