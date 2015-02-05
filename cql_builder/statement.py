from cassandra import ConsistencyLevel as Level
from cassandra.query import SimpleStatement
from cql_builder.base import Statement, Assignment, ValidationError
from cql_builder.condition import Where, Using, Limit
from cql_builder.assignment import Set, SetAt, Add, Subtract
from cql_builder.selection import Columns, ValueAt, Count, All

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
		self.validate()
		statement = 'INSERT INTO {}.{} ({}) VALUES ({})'
		names = ', '.join(self.assignment.kwargs.keys())
		values = ', '.join('%s' for k in self.assignment.values)
		query = statement.format(self.keyspace, self.column_family, names, values)
		if self.not_exists:
			query = '{} IF NOT EXISTS'.format(query)
		if self.options:
			query = '{} {}'.format(query, self.options.cql)		
		return query

	def statement(self, consistency=Level.ONE):
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

	def set(self, **kwargs):
		self.assignment = Set(**kwargs)
		return self

	def set_at(self, name, key, value):
		self.assignment = SetAt(name, key, value)
		return self

	def add(self, name, value):
		self.assignment = Add(name, value)
		return self

	def subtract(self, name, value):
		self.assignment = Subtract(name, value)
		return self

	def where(self, *args):
		self.conditions = Where(*args)
		return self

	@property
	def cql(self):
		self.validate()
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

	def validate(self):
		if self.conditions is None:
			raise ValidationError('conditions: {}'.format(self.conditions))
		if self.assignment is None:
			raise ValidationError('assignment: {}'.format(self.assignment))

class Select(Statement):

	def __init__(self, keyspace, column_family):
		Statement.__init__(self, keyspace, column_family)
		self.selection = None
		self.conditions = None
		self.lim = None

	def columns(self, *args):
		self.selection = Columns(*args)
		return self

	def all(self):
		self.selection = All()
		return self

	def count(self):
		self.selection = Count()
		return self

	def where(self, *args):
		self.conditions = Where(*args)
		return self

	def limit(self, value):
		self.lim = Limit(value)
		return self

	@property
	def cql(self):
		self.validate()
		statement = 'SELECT {} FROM {}.{}'
		query = statement.format(self.selection.cql, self.keyspace, self.column_family)
		if self.conditions:
			query = '{} WHERE {}'.format(query, self.conditions.cql)
		if self.lim:
			query = '{} {}'.format(query, self.lim.cql)
		return query

	def statement(self, consistency=Level.ONE):
		select = SimpleStatement(self.cql, consistency_level=consistency)
		args = list(self.selection.values)
		if self.conditions:
			args.extend(self.conditions.values)
		if self.lim:
			args.extend(self.lim.values)
		return select, args

	def validate(self):
		if self.selection is None:
			raise ValidationError('selection: {}'.format(self.selection))

class Delete(Statement):

	def __init__(self, keyspace, column_family):
		Statement.__init__(self, keyspace, column_family)
		self.selection = None
		self.conditions = None

	def columns(self, *args):
		self.selection = Columns(*args)
		return self

	def at(self, name, key):
		self.selection = ValueAt(name, key)
		return self

	def where(self, *args):
		self.conditions = Where(*args)
		return self

	@property
	def cql(self):
		self.validate()
		query = 'DELETE'
		if self.selection:
			query = '{} {}'.format(query, self.selection.cql)
		query = '{} FROM {}.{} WHERE {}'.format(query, self.keyspace, self.column_family, self.conditions.cql)
		return query

	def statement(self, consistency=Level.ONE):
		delete = SimpleStatement(self.cql, consistency_level=consistency)
		args = []
		if self.selection:
			args.extend(self.selection.values)
		args.extend(self.conditions.values)
		return delete, args

	def validate(self):
		if self.conditions is None:
			raise ValidationError('conditions: {}'.format(self.conditions))
