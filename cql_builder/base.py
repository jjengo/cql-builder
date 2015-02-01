from cassandra import ConsistencyLevel as Level

class QueryItem(object):
	@property
	def cql(self):
		raise NotImplementedError('cql not implemented')

class Assignment(QueryItem):
	@property
	def values(self):
		raise NotImplementedError('values not implemented')

class Condition(QueryItem):
	@property
	def values(self):
		raise NotImplementedError('values not implemented')

class Statement(QueryItem):
	def __init__(self, keyspace, column_family):
		self.keyspace = keyspace
		self.column_family = column_family	
	def statement(self, consistency=Level.ONE):
		raise NotImplementedError('statement not implemented')
	def validate(self):
		if not self.keyspace:
			raise ValidationError('keyspace={}'.format(self.keyspace))
		if not self.column_family:
			raise ValidationError('column_family={}'.format(self.column_family))

class ValidationError(ValueError):
	pass
