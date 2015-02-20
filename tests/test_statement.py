import unittest
from unittest import TestCase
from cql_builder.base import ValidationError
from cql_builder.selection import Columns
from cql_builder.condition import Using, Where, Limit, eq
from cql_builder.assignment import Assignments, Set
from cql_builder.statement import Insert, Update, Select, Delete

class TestInsert(TestCase):

	def setUp(self):
		self.keyspace = 'test_keyspace'
		self.column_family = 'test_column_family'

	def get_query(self, kwargs):
		query = 'INSERT INTO {}.{} ({}) VALUES ({})'
		names = ', '.join(kwargs.keys())
		values = ', '.join('%s' for k in kwargs.values())
		return query.format(self.keyspace, self.column_family, names, values)

	def test_no_assignment(self):
		op = Insert(self.keyspace, self.column_family)
		self.assertRaises(ValidationError, op.statement)

	def test_valid(self):
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

class TestUpdate(TestCase):

	def setUp(self):
		self.keyspace = 'test_keyspace'
		self.column_family = 'test_column_family'

	def get_query(self, assignment, condition, using=None):
		query = 'UPDATE {}.{}'.format(self.keyspace, self.column_family)
		if using:
			query = '{} {}'.format(query, using.cql)
		assignments = Assignments()
		assignments.add(assignment)
		where = Where(condition)
		return '{} SET {} WHERE {}'.format(query, assignments.cql, where.cql)

	def test_no_assignment(self):
		op = (Update(self.keyspace, self.column_family)
			.where(eq('name', 'foo'))
		)
		self.assertRaises(ValidationError, op.statement)

	def test_no_condition(self):
		op = (Update(self.keyspace, self.column_family)
			.set(name='foo')
		)
		self.assertRaises(ValidationError, op.statement)

	def test_valid(self):
		assignment = Set(first='foo')
		condition = eq('last', 'bar')
		op = (Update(self.keyspace, self.column_family)
			.set(**assignment.kwargs)
			.where(condition)
		)
		statement, args = op.statement()
		query = self.get_query(assignment, condition)
		self.assertEquals(statement.query_string, query)
		self.assertEquals(args, assignment.values + condition.values)

	def test_options(self):
		assignment = Set(first='foo')
		condition = eq('last', 'bar')
		using = Using(ttl=10800)
		op = (Update(self.keyspace, self.column_family)
			.using(**using.options)
			.set(**assignment.kwargs)
			.where(condition)
		)
		statement, args = op.statement()
		query = self.get_query(assignment, condition, using)
		self.assertEquals(statement.query_string, query)
		self.assertEquals(args, using.values + assignment.values + condition.values)

class TestSelect(TestCase):

	def setUp(self):
		self.keyspace = 'test_keyspace'
		self.column_family = 'test_column_family'

	def get_query(self, selection, condition=None):
		query = 'SELECT {} FROM {}.{}'
		query = query.format(selection.cql, self.keyspace, self.column_family)
		if condition:
			where = Where(condition)
			query = '{} WHERE {}'.format(query, where.cql)
		return query

	def test_no_selection(self):
		op = Select(self.keyspace, self.column_family)
		self.assertRaises(ValidationError, op.statement)

	def test_selection(self):
		selection = Columns('first', 'last')
		op = (Select(self.keyspace, self.column_family)
			.columns(*selection.args)
		)
		statement, args = op.statement()
		query = self.get_query(selection)
		self.assertEquals(statement.query_string, query)
		self.assertEquals(args, selection.values)

	def test_condition(self):
		selection = Columns('first', 'last')
		condition = eq('name', 'foo')
		op = (Select(self.keyspace, self.column_family)
			.columns(*selection.args)
			.where(condition)
		)
		statement, args = op.statement()
		query = self.get_query(selection, condition)
		self.assertEquals(statement.query_string, query)
		self.assertEquals(args, selection.values + condition.values)

	def test_limit(self):
		selection = Columns('first', 'last')
		limit = Limit(5)
		op = (Select(self.keyspace, self.column_family)
			.columns(*selection.args)
			.limit(limit.value)
		)
		statement, args = op.statement()
		query = '{} {}'.format(self.get_query(selection), limit.cql)
		self.assertEquals(statement.query_string, query)
		self.assertEquals(args, selection.values + limit.values)

if __name__ == '__main__':
	unittest.main()
