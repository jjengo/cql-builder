from cql_builder.base import Condition

# condition AND condition AND ...
class Where(Condition):
	def __init__(self, *args):
		self.conditions = args
	@property
	def cql(self):
		return ' AND '.join(cond.cql for cond in self.conditions)
	@property
	def values(self):
		value_list = []
		for cond in self.conditions:
			value_list.extend(cond.values)
		return value_list

# USING option AND option AND ...
class Using(Condition):
	def __init__(self, **kwargs):
		self.options = {k.upper(): v for k, v in kwargs.iteritems()}
	@property
	def cql(self):
		pairs = ' AND '.join('{} %s'.format(k) for k in self.options.keys())
		return 'USING {}'.format(pairs)
	@property
	def values(self):
		return self.options.values()

# name-comparator-value
class Comparison(Condition):
	def __init__(self, name, value, compare):
		self.name = name
		self.value = value
		self.compare = compare
	@property
	def cql(self):
		return '{}{}%s'.format(self.name, self.compare)
	@property
	def values(self):
		return [self.value]

# name IN {value, value, ...}
class In(Condition):
	def __init__(self, name, value):
		self.name = name
		self.value = value
	@property
	def cql(self):
		in_list = ', '.join('%s' for k in self.value)
		return '{} IN ({})'.format(self.name, in_list)
	@property
	def values(self):
		return self.value

class All(Condition):
	def __init__(self, **kwargs):
		self.kwargs = kwargs
	@property
	def cql(self):
		return ' AND '.join('{}=%s'.format(k) for k in self.kwargs.keys())
	@property
	def values(self):
		return self.kwargs.values()

# Condition helpers.
def eq(name, value):
	return Comparison(name, value, '=')

def gt(name, value):
	return Comparison(name, value, '>')

def gte(name, value):
	return Comparison(name, value, '>=')

def lt(name, value):
	return Comparison(name, value, '<')

def lte(name, value):
	return Comparison(name, value, '<=')

def within(name, collection):
	return In(name, collection)

def all_eq(**kwargs):
	return All(**kwargs)
