import unittest
from unittest import TestCase
from cql_builder.selection import Columns, ValueAt, All, Count

class TestColumns(TestCase):

	def test_single(self):
		name = ['foo']
		columns = Columns(*name)
		self.assertEquals(columns.cql, name[0])

	def test_multi(self):
		names = ['foo', 'bar']
		columns = Columns(*names)
		self.assertEquals(columns.cql, ', '.join(names))

class TestValueAt(TestCase):
	def test_valid(self):
		name, key = 'foo', 'bar'
		at = ValueAt(name, key)
		self.assertEquals(at.cql, '{}[%s]'.format(name))
		self.assertEquals(at.values, [key])

class TestCount(TestCase):
	def test_valid(self):
		count = Count()
		self.assertEquals(count.cql, 'COUNT(*)')

class TestAll(TestCase):
	def test_valid(self):
		self.assertEquals(All().cql, '*')
