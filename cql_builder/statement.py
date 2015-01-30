from cassandra import ConsistencyLevel as Level
from cassandra.query import SimpleStatement
from cql_builder.base import QueryItem, Statement
from cql_builder.condition import Where, Using

class Insert(Statement):

	def __init__(self, keyspace, column_family):
		self.keyspace = keyspace
		self.column_family = column_family
		self.value_map = {}
		self.options = None
		self.not_exists = False

	def value(self, name, value):
		self.value_map[name] = value
		return self

	def values(self, **kwargs):
		self.value_map = kwargs
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
		names = ', '.join(self.value_map.keys())
		values = ', '.join(map(lambda x: '%s', self.value_map.keys()))
		query = statement.format(self.keyspace, self.column_family, names, values)
		if self.not_exists:
			query = '{} {}'.format(query, 'IF NOT EXISTS')
		if self.options:
			query = '{} {}'.format(query, self.options.cql)		
		return query

	def statement(self, consistency=Level.ONE):
		insert = SimpleStatement(self.cql, consistency_level=consistency)
		args = self.value_map.values()
		if self.options:
			args.extend(self.options.values)
		return insert, args

class Update(Statement):

	def __init__(self, keyspace, column_family):
		self.keyspace = keyspace
		self.column_family = column_family
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
		update = SimpleStatement(self.cql, consistency_level=consistency)
		args = self.options.values if self.options else []
		args.extend(self.assignment.values)
		args.extend(self.conditions.values)
		return update, args
