#Function class
class objFunction():
	def __init__(self, id, name, params, data_type, privacy):
		self.id = id
		self.name = name
		self.params = params
		self.data_type = data_type
		self.tempVars = []
		self.privacy = privacy
