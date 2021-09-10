
# Classe que trata e agrupa os dados das medições
class ControlLevels:
	
	list_patients = None
	
	default_score = 0

	def __init__(self, list_patients):
		self.list_patients = list_patients
		self.priority_high = []
		self.priority_medium = []
		self.priority_normal = []
		
	def process(self):
		list_patients_on = []
		
		priority_normal = []
		priority_medium = []
		priority_high = []
		
		for index in self.list_patients:
			if(self.list_patients[index]['medicao']):
				list_patients_on.append([self.default_score, self.list_patients[index]])
		
		for patient in list_patients_on:
			if(int(patient[1]['saturacao']) > 95):
				priority_normal.append(patient)
			elif(int(patient[1]['saturacao']) >= 93 and int(patient[1]['saturacao']) <= 95):
				priority_medium.append(patient)
			else:
				priority_high.append(patient)
		
		high = self.sort(priority_high)
		medium = self.sort(priority_medium)
		normal = self.sort(priority_normal)
		
		return {'high': high, 'medium': medium, 'normal': normal}
				
	def sort(self, list_patients):
		new_list = []
		for patient in list_patients:
			
			# Idade
			if(int(patient[1]['idade']) >= 60):
				patient[0] = patient[0] + 30
			elif(int(patient[1]['idade']) >= 50 and int(patient[1]['idade']) < 60):
				patient[0] = patient[0] + 20
			elif(int(patient[1]['idade']) >= 30 and int(patient[1]['idade']) < 50):
				patient[0] = patient[0] + 8
			elif(int(patient[1]['idade']) > 0 and int(patient[1]['idade']) < 30):
				patient[0] = patient[0] + 7
			
			# Saturacao
			if(patient[1]['saturacao'] <= 80):
				patient[0] = patient[0] + 30
			elif(patient[1]['saturacao'] > 80 and patient[1]['saturacao'] <= 90):
				patient[0] = patient[0] + 20
			elif(patient[1]['saturacao'] > 90 and patient[1]['saturacao'] <= 95):
				patient[0] = patient[0] + 5
				
			# Temperatura
			if(float(patient[1]['temperatura'].replace(',', '.')) > 37.5):
				patient[0] = patient[0] + 10
			elif(float(patient[1]['temperatura'].replace(',', '.')) < 36.0):
				patient[0] = patient[0] + 8
				
			# Pressao
			if(int(patient[1]['pressao']) >= 130):
				patient[0] = patient[0] + 10
				
			# Batimentos
			if(int(patient[1]['batimento']) > 90 or int(patient[1]['batimento']) < 50):
				patient[0] = patient[0] + 10
			
			new_list.append(patient)
		
		new_list.sort(reverse=True, key=self.valueSort)
		patients = []
		for patient in new_list:
			patients.append(patient[1])
		return patients
		
	def valueSort(self, el):
		return el[0]
			
				
			
	