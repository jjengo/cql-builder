from cassandra import ConsistencyLevel as Level
from cassandra.query import SimpleStatement
from cql_builder.base import Statement, Assignment, ValidationError
from cql_builder.condition import Where, Using
from cql_builder.assignment import Set

class Insert(Statement):

	def __init__(self, keyspace, column_family):
		Statement.__init__(self, keyspace, column_family)
		self.assignment = None
		self.options = None
		self.not_exists = False

	def values(self, **kwargs):
		self.assignment = Set(**kwargs)
		return self

	def using(self, **kwargs):
		self.options = Using(**kwargs)
		return self

	def if_not_exists(self):
		self.not_exists = True
		return self

	@property
	def cql(self):
		statement = 'INSERT INTO {}.{} ({}) VALUES ({})'
		names = ', '.join(self.assignment.kwargs.keys())
		values = ', '.join('%s' for k in self.assignment.values)
		query = statement.format(self.keyspace, self.column_family, names, values)
		if self.not_exists:
			query = '{} {}'.format(query, 'IF NOT EXISTS')
		if self.options:
			query = '{} {}'.format(query, self.options.cql)		
		return query

	def statement(self, consistency=Level.ONE):
		self.validate()
		insert = SimpleStatement(self.cql, consistency_level=consistency)
		args = list(self.assignment.values)
		if self.options:
			args.extend(self.options.values)
		return insert, args

	def validate(self):
		if self.assignment is None:
			raise ValidationError('insert assignment: {}'.format(self.assignment))

class Update(Statement):

	def __init__(self, keyspace, column_family):
		Statement.__init__(self, keyspace, column_family)
		self.assignment = None
		self.conditions = None
		self.options = None

	def using(self, **kwargs):
		self.options = Using(**kwargs)
		return self

	def set(self, assignment):
		self.assignment = assignment
		return self

	def where(self, *args):
		self.conditions = Where(*args)
		return self

	@property
	def cql(self):
		query = 'UPDATE {}.{}'.format(self.keyspace, self.column_family)
		if self.options:
			query = '{} {}'.format(query, self.options.cql)
		query = '{} SET {} WHERE {}'.format(query, self.assignment.cql, self.conditions.cql)
		return query

	def statement(self, consistency=Level.ONE):
		self.validate()
		update = SimpleStatement(self.cql, consistency_level=consistency)
		args = self.options.values if self.options else []
		args.extend(self.assignment.values)
		args.extend(self.conditions.values)
		return update, args

	def validate(self):
		if self.conditions is None:
			raise ValidationError('update conditions: {}'.format(self.conditions))
		if self.assignment is None or not isinstance(self.assignment, Assignment):
			raise ValidationError('update assignment: {}'.format(self.assignment))
