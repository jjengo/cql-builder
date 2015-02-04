from cql_builder.base import Selection

class Columns(Selection):
	def __init__(self, *args):
		self.args = args
	@property
	def cql(self):
		return ', '.join(self.args)

class Count(Selection):
	@property
	def cql(self):
		return 'COUNT(*)'

class All(Selection):
	@property
	def cql(self):
		return '*'
