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
	def __init__(self, column_family, keyspace=None):
		self.column_family = column_family
		self.keyspace = keyspace
	@property
	def path(self):
		if self.keyspace:
			return '{}.{}'.format(self.keyspace, self.column_family)
		else:
			return self.column_family
	@property
	def args(self):
		return []
	def validate(self):
		pass
	def statement(self):
		self.validate()
		return self.cql, self.args

class ValidationError(ValueError):
	pass
