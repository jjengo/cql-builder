from cql_builder.base import Assignment, ValidationError

# {key=value, key=value, ...}
class Set(Assignment):
	def __init__(self, **kwargs):
		self.kwargs = kwargs
	@property
	def cql(self):
		return ', '.join('{}=%s'.format(k) for k in self.kwargs.keys())
	@property
	def values(self):
		return self.kwargs.values()

# names['foo'] = 'bar'
# names[2] = 'foo'
class SetAt(Assignment):
	def __init__(self, name, key, value):
		self.name = name
		self.key = key
		self.value = value
	@property
	def cql(self):
		return '{}[%s] = %s'.format(self.name)
	@property
	def values(self):
		return [self.key, self.value]

# name = name + {value, value, ...}
# name = name + [value, value, ...]
class Add(Assignment):
	def __init__(self, name, value):
		self.name = name
		self.value = value
	@property
	def cql(self):
		return '{}={} + %s'.format(self.name, self.name)
	@property
	def values(self):
		return [self.value]

# name = name - {value, value, ...}
# name = name - [value, value, ...]
class Subtract(Assignment):
	def __init__(self, name, value):
		self.name = name
		self.value = value
	@property
	def cql(self):
		return '{}={} - %s'.format(self.name, self.name)
	@property
	def values(self):
		return [self.value]

# assignment, assignment, ...
class Assignments(Assignment):
	def __init__(self):
		self.assignments = []
	def add(self, *assignment):
		self.assignments.extend(assignment)
	@property
	def cql(self):
		return ', '.join(assign.cql for assign in self.assignments)
	@property
	def values(self):
		value_list = []
		for assign in self.assignments:
			value_list.extend(assign.values)
		return value_list
	def validate(self):
		if not self.assignments:
			raise ValidationError('assignments is empty')
		for assign in self.assignments:
			if assign is None:
				raise ValidationError('assignment: {}'.format(assign))
			if not isinstance(assign, Assignment):
				raise ValidationError('assignment {!r} must be of type Assignment'.format(assign))
