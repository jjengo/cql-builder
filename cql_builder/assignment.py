from cql_builder.base import Assignment

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

# name = name + {value, value, ...}
# name = name + [value, value, ...]
# TODO - check maps
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
# TODO check maps
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
