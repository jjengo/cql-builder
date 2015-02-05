from cql_builder.base import Selection

class Columns(Selection):
	def __init__(self, *args):
		self.args = args
	@property
	def cql(self):
		return ', '.join(self.args)
	@property
	def values(self):
		return []

class ValueAt(Selection):
	def __init__(self, name, key):
		self.name = name
		self.key = key
	@property
	def cql(self):
		return '{}[%s]'.format(self.name)
	@property
	def values(self):
		return [self.key]

class Count(Selection):
	@property
	def cql(self):
		return 'COUNT(*)'
	@property
	def values(self):
		return []

class All(Selection):
	@property
	def cql(self):
		return '*'
	@property
	def values(self):
		return []
