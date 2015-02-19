from cassandra import ConsistencyLevel as Level

class Expression(object):
	@property
	def cql(self):
		raise NotImplementedError('cql not implemented')

class Assignment(Expression):
	@property
	def values(self):
		raise NotImplementedError('values not implemented')

class Condition(Expression):
	@property
	def values(self):
		raise NotImplementedError('values not implemented')

class Selection(Expression):
	@property
	def values(self):
		raise NotImplementedError('values not implemented')

class Statement(Expression):
	def __init__(self, keyspace, column_family):
		self.keyspace = keyspace
		self.column_family = column_family	
	def statement(self, consistency=Level.ONE):
		raise NotImplementedError('statement not implemented')

class ValidationError(ValueError):
	pass
