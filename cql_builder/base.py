from cassandra import ConsistencyLevel as Level

class QueryItem(object):
	@property
	def cql(self):
		raise NotImplementedError('QueryItem: cql not implemented')

class Assignment(QueryItem):
	@property
	def values(self):
		raise NotImplementedError('Assignment: values not implemented')

class Condition(QueryItem):
	@property
	def values(self):
		raise NotImplementedError('Conditional: values not implemented')

class Statement(QueryItem):
	def statement(self, consistency=Level.ONE):
		raise NotImplementedError('QueryStatement: statement not implemented')

