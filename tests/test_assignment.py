import unittest
from unittest import TestCase
from cql_builder.assignment import Set, Add, Subtract

class TestSet(TestCase):

	def test_value_single(self):
		op = Set(name='foo')
		self.assertEquals(op.cql, 'name=%s')
		self.assertEquals(op.values, ['foo'])

	def test_value_multi(self):
		kwargs = {'first': 'foo', 'last': 'bar'}
		op = Set(**kwargs)
		self.assertEquals(op.cql, '{}=%s, {}=%s'.format(*kwargs.keys()))
		self.assertEquals(op.values, kwargs.values())

class TestAdd(TestCase):

	def test_value(self):
		name, value = 'name', ['foo', 'bar']
		op = Add(name, value)
		self.assertEquals(op.cql, '{}={} + %s'.format(name, name))
		self.assertEquals(op.values, [value])

class TestSubtract(TestCase):

	def test_value(self):
		name, value = 'name', ['foo', 'bar']
		op = Subtract(name, value)
		self.assertEquals(op.cql, '{}={} - %s'.format(name, name))
		self.assertEquals(op.values, [value])	

if __name__ == '__main__':
	unittest.main()
