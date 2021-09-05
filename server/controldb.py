import os
import sys
import json

class ControlDB:
	db_path = '\\server\\database\\'
	db_name = 'database'
	db_extension = '.json'
	
	def insert(self, data):
		new_data = {'nome': data['nome'], 'saturacao': data['saturacao'], 'pressao': data['pressao'], 'batimentos': data['batimentos']}
		current_data = self.getAll()
		new_id = int(self.getLastId()) + 1
		current_data[str(new_id)] = new_data
		with open(os.getcwd() + self.db_path + self.db_name + self.db_extension, 'w', encoding='utf-8') as db_write:
			json.dump(current_data, db_write, ensure_ascii=False, indent=4)
		return new_id
	
	def getLastId(self):
		last_id = -1
		with open(os.getcwd() + self.db_path + self.db_name + self.db_extension, 'r', encoding='utf-8') as db_read:
			data = json.load(db_read)
			for id in data:
				last_id = id
		return last_id
	
	def getAll(self):
		data = None
		with open(os.getcwd() + self.db_path + self.db_name + self.db_extension, 'r', encoding='utf-8') as db_read:
			data = json.load(db_read)
		return json.dumps(data)
	
	def get(self, id):
		with open(os.getcwd() + self.db_path + self.db_name + self.db_extension, 'r', encoding='utf-8') as db_read:
			data_read = json.load(db_read)
			for id_read in data_read:
				if(str(id_read) == str(id)):
					return json.dumps(data_read[id_read])
		return None
	
	def has(self, id):
		with open(os.getcwd() + self.db_path + self.db_name + self.db_extension, 'r', encoding='utf-8') as db_read:
			data_read = json.load(db_read)
			for id_read in data_read:
				if(str(id_read) == str(id)):
					return True
		return False
		
	def update(self, id, data):
		if(not self.has(id)):
			return False
			
		with open(os.getcwd() + self.db_path + self.db_name + self.db_extension, 'r', encoding='utf-8') as db_read:
			data_read = json.load(db_read)
			for id_read in data_read:
				if(str(id_read) == str(id)):
					data_read[id_read] = data
					with open(os.getcwd() + self.db_path + self.db_name + self.db_extension, 'w', encoding='utf-8') as db_write:
						json.dump(data_read, db_write, ensure_ascii=False, indent=4)
					return True
		return False	
		
	def updateAttribute(self, id, attr, value):
		if(not self.has(id)):
			return False
			
		with open(os.getcwd() + self.db_path + self.db_name + self.db_extension, 'r', encoding='utf-8') as db_read:
			data_read = json.load(db_read)
			for id_read in data_read:
				if(str(id_read) == str(id)):
					data_read[id_read][attr] = value
					with open(os.getcwd() + self.db_path + self.db_name + self.db_extension, 'w', encoding='utf-8') as db_write:
						json.dump(data_read, db_write, ensure_ascii=False, indent=4)
					return True
		return False	