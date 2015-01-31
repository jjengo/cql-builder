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
		self.kwargs = kwargs
	@property
	def cql(self):
		pairs = ' AND '.join(map(lambda x: '{} %s'.format(x), self.kwargs.keys()))
		return 'USING {}'.format(pairs)
	@property
	def values(self):
		return self.kwargs.values()

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
	def __init__(self, name, collection):
		self.name = name
		self.collection = collection
	@property
	def cql(self):
		in_list = ', '.join(map(lambda x: '%s', self.collection))
		return '{} IN ({})'.format(self.name, in_list)
	@property
	def values(self):
		return self.collection

class All(Condition):
	def __init__(self, **kwargs):
		self.kwargs = kwargs
	@property
	def cql(self):
		return ' AND '.join(map(lambda x: '{}=%s'.format(x), self.kwargs.keys()))
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
