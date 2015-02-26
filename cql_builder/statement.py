from cql_builder.base import Statement, ValidationError
from cql_builder.condition import Where, Using, Limit
from cql_builder.assignment import Assignments, Set, SetAt, Add, Subtract
from cql_builder.selection import Columns, ValueAt, Count, All

class Insert(Statement):

	def __init__(self, column_family, keyspace=None):
		Statement.__init__(self, column_family, keyspace)
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
		statement = 'INSERT INTO {} ({}) VALUES ({})'
		names = ', '.join(self.assignment.kwargs.keys())
		values = ', '.join('%s' for k in self.assignment.values)
		query = statement.format(self.path, names, values)
		if self.not_exists:
			query = '{} IF NOT EXISTS'.format(query)
		if self.options:
			query = '{} {}'.format(query, self.options.cql)		
		return query

	@property
	def args(self):
		args = list(self.assignment.values)
		if self.options:
			args.extend(self.options.values)
		return args

	def validate(self):
		if self.assignment is None:
			raise ValidationError('insert assignment: {}'.format(self.assignment))

class Update(Statement):

	def __init__(self, column_family, keyspace=None):
		Statement.__init__(self, column_family, keyspace)
		self.assignments = Assignments()
		self.conditions = None
		self.options = None

	def using(self, **kwargs):
		self.options = Using(**kwargs)
		return self

	def set(self, **kwargs):
		self.assignments.add(Set(**kwargs))
		return self

	def set_at(self, name, key, value):
		self.assignments.add(SetAt(name, key, value))
		return self

	def add(self, name, value):
		self.assignments.add(Add(name, value))
		return self

	def subtract(self, name, value):
		self.assignments.add(Subtract(name, value))
		return self

	def where(self, *args):
		self.conditions = Where(*args)
		return self

	@property
	def cql(self):
		query = 'UPDATE {}'.format(self.path)
		if self.options:
			query = '{} {}'.format(query, self.options.cql)
		query = '{} SET {} WHERE {}'.format(query, self.assignments.cql, self.conditions.cql)
		return query

	@property
	def args(self):
		args = self.options.values if self.options else []
		args.extend(self.assignments.values)
		args.extend(self.conditions.values)
		return args

	def validate(self):
		self.assignments.validate()
		if self.conditions is None:
			raise ValidationError('conditions: {}'.format(self.conditions))

class Select(Statement):

	def __init__(self, column_family, keyspace=None):
		Statement.__init__(self, column_family, keyspace)
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
		query = 'SELECT {} FROM {}'.format(self.selection.cql, self.path)
		if self.conditions:
			query = '{} WHERE {}'.format(query, self.conditions.cql)
		if self.lim:
			query = '{} {}'.format(query, self.lim.cql)
		return query

	@property
	def args(self):
		args = list(self.selection.values)
		if self.conditions:
			args.extend(self.conditions.values)
		if self.lim:
			args.extend(self.lim.values)
		return args

	def validate(self):
		if self.selection is None:
			raise ValidationError('selection: {}'.format(self.selection))

class Delete(Statement):

	def __init__(self, column_family, keyspace=None):
		Statement.__init__(self, column_family, keyspace)
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
		query = 'DELETE'
		if self.selection:
			query = '{} {}'.format(query, self.selection.cql)
		query = '{} FROM {} WHERE {}'.format(query, self.path, self.conditions.cql)
		return query

	@property
	def args(self):
		args = []
		if self.selection:
			args.extend(self.selection.values)
		args.extend(self.conditions.values)
		return args

	def validate(self):
		if self.conditions is None:
			raise ValidationError('conditions: {}'.format(self.conditions))

class Truncate(Statement):

	def __init__(self, column_family, keyspace=None):
		Statement.__init__(self, column_family, keyspace)

	@property
	def cql(self):
		return 'TRUNCATE {}'.format(self.path)

