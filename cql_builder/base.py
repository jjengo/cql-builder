from cassandra import ConsistencyLevel as Level

class QueryItem(object):
	@property
	def cql(self):
		raise NotImplementedError('cql not implemented')
	def validate(self):
		raise NotImplementedError('validate not implemented')

class Assignment(QueryItem):
	@property
	def values(self):
		raise NotImplementedError('values not implemented')

class Condition(QueryItem):
	@property
	def values(self):
		raise NotImplementedError('values not implemented')

class Statement(QueryItem):
	def statement(self, consistency=Level.ONE):
		raise NotImplementedError('QueryStatement: statement not implemented')

class ValidationError(ValueError):
	pass
