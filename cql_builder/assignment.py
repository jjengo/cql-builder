from cql_builder.base import Assignment, ValidationError

# {key=value, key=value, ...}
class Set(Assignment):
	def __init__(self, **kwargs):
		self.kwargs = kwargs
		self.validate()
	@property
	def cql(self):
		return ', '.join('{}=%s'.format(k) for k in self.kwargs.keys())
	@property
	def values(self):
		return self.kwargs.values()
	def validate(self):
		if not self.kwargs:
			raise ValidationError('Assignments are empty')
		for k, v in self.kwargs.iteritems():
			if not v:
				raise ValidationError('{}={}'.format(k, v))

# name = name + {value, value, ...}
# name = name + [value, value, ...]
# TODO - check maps
class Add(Assignment):
	def __init__(self, name, value):
		self.name = name
		self.value = value
		self.validate()
	@property
	def cql(self):
		return '{}={} + %s'.format(self.name, self.name)
	@property
	def values(self):
		return [self.value]
	def validate(self):
		if not self.name or not self.value:
			raise ValidationError('{}={} + {}'.format(self.name, self.name, self.value))
		if not isinstance(self.value, list) or not isinstance(self.value, set):
			raise ValidationError('{} is not a list or set'.format(self.value))

# name = name - {value, value, ...}
# name = name - [value, value, ...]
# TODO check maps
class Subtract(Assignment):
	def __init__(self, name, value):
		self.name = name
		self.value = value
		self.validate()
	@property
	def cql(self):
		return '{}={} - %s'.format(self.name, self.name)
	@property
	def values(self):
		return [self.value]
	def validate(self):
		if not self.name or not self.value:
			raise ValidationError('{}={} - {}'.format(self.name, self.name, self.value))
		if not isinstance(self.value, list) or not isinstance(self.value, set):
			raise ValidationError('{} if not a list or set'.format(self.value))
