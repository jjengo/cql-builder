import unittest
from unittest import TestCase
from cql_builder.base import ValidationError
from cql_builder.condition import Using
from cql_builder.assignment import Set
from cql_builder.statement import Insert, Update, Select, Delete

class TestInsert(TestCase):

	def setUp(self):
		self.keyspace = 'test_keyspace'
		self.column_family = 'test_column_family'
		self.query_base = 'INSERT INTO {}.{}'.format(self.keyspace, self.column_family)

	def get_query(self, kwargs):
		query = 'INSERT INTO {}.{} ({}) VALUES ({})'
		names = ', '.join(kwargs.keys())
		values = ', '.join('%s' for k in kwargs.values())
		return query.format(self.keyspace, self.column_family, names, values)

	def test_no_assignment(self):
		op = Insert(self.keyspace, self.column_family)
		self.assertRaises(ValidationError, op.statement)

	def test_value_single(self):
		assignment = {'name': 'foo'}
		op = (Insert(self.keyspace, self.column_family)
			.values(**assignment)
		)
		statement, args = op.statement()
		self.assertEquals(statement.query_string, self.get_query(assignment))
		self.assertEquals(args, assignment.values())

	def test_value_multi(self):
		assignment = {'first': 'foo', 'last': 'bar', 'age': 13}
		op = (Insert(self.keyspace, self.column_family)
			.values(**assignment)
		)
		statement, args = op.statement()
		self.assertEquals(statement.query_string, self.get_query(assignment))
		self.assertEquals(args, assignment.values())		

	def test_options(self):
		assignment = {'name': 'foo'}
		using = Using(ttl=10800)
		op = (Insert(self.keyspace, self.column_family)
			.values(**assignment)
			.using(**using.options)
		)
		statement, args = op.statement()
		query = '{} {}'.format(self.get_query(assignment), using.cql)
		self.assertEquals(statement.query_string, query)
		self.assertEquals(args, assignment.values() + using.values)

	def test_if_not_exists(self):
		assignment = {'name': 'foo'}
		op = (Insert(self.keyspace, self.column_family)
			.values(**assignment)
			.if_not_exists()
		)
		statement, args = op.statement()
		query = '{} IF NOT EXISTS'.format(self.get_query(assignment))
		self.assertEquals(statement.query_string, query)
		self.assertEquals(args, assignment.values())

if __name__ == '__main__':
	unittest.main()
