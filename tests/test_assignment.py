import unittest
from unittest import TestCase
from cql_builder.base import ValidationError
from cql_builder.condition import eq
from cql_builder.assignment import Set, SetAt, Add, Subtract, Assignments

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

class TestSetAt(TestCase):

	def test_value(self):
		op = SetAt('name', 0, 'foo')
		self.assertEquals(op.cql, 'name[%s] = %s')
		self.assertEquals(op.values, [0, 'foo'])

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

class TestAssignments(TestCase):

	def test_no_values(self):
		op = Assignments()
		self.assertRaises(ValidationError, op.validate)

	def test_none_value(self):
		op = Assignments()
		op.add(Set(name='foo'))
		op.add(None)
		self.assertRaises(ValidationError, op.validate)

	def test_invalid_instance_value(self):
		op = Assignments()
		op.add(Set(name='foo'))
		op.add(eq('name', 'bar'))
		self.assertRaises(ValidationError, op.validate)

	def test_value_single(self):
		op = Assignments()
		kwargs = {'name': 'bar'}
		op.add(Set(**kwargs))
		self.assertEquals(op.cql, '{}=%s'.format(*kwargs.keys()))
		self.assertEquals(op.values, kwargs.values())

	def test_value_multi(self):
		op = Assignments()
		op1 = Set(first='foo')
		op2 = Set(last='bar')
		op.add(op1, op2)
		self.assertEquals(op.cql, '{}, {}'.format(op1.cql, op2.cql))
		self.assertEquals(op.values, op1.values + op2.values)

if __name__ == '__main__':
	unittest.main()
