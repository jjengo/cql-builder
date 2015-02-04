import unittest
from unittest import TestCase
from cql_builder.selection import Columns, All, Count

class TestColumns(TestCase):

	def test_single(self):
		name = ['foo']
		columns = Columns(*name)
		self.assertEquals(columns.cql, name[0])

	def test_multi(self):
		names = ['foo', 'bar']
		columns = Columns(*names)
		self.assertEquals(columns.cql, ', '.join(names))

class TestCount(TestCase):
	def test_valid(self):
		count = Count()
		self.assertEquals(count.cql, 'COUNT(*)')

class TestAll(TestCase):
	def test_valid(self):
		self.assertEquals(All().cql, '*')
