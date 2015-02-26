import unittest
from unittest import TestCase
from cql_builder.base import Statement, ValidationError
from cql_builder.selection import Columns
from cql_builder.condition import Using, Where, Limit, eq
from cql_builder.assignment import Assignments, Set
from cql_builder.statement import Insert, Update, Select, Delete, Truncate

class TestStatement(TestCase):

	def test_full_path(self):
		keyspace = 'test_keyspace'
		column_family = 'test_column_family'
		path = '{}.{}'.format(keyspace, column_family)
		statement = Statement(column_family, keyspace)
		self.assertEquals(statement.path, path)

	def test_partial_path(self):
		column_family = 'test_column_family'
		statement = Statement(column_family)
		self.assertEquals(statement.path, column_family)

class TestInsert(TestCase):

	def setUp(self):
		self.column_family = 'test_column_family'

	def get_query(self, kwargs):
		query = 'INSERT INTO {} ({}) VALUES ({})'
		names = ', '.join(kwargs.keys())
		values = ', '.join('%s' for k in kwargs.values())
		return query.format(self.column_family, names, values)

	def test_no_assignment(self):
		op = Insert(self.column_family)
		self.assertRaises(ValidationError, op.statement)

	def test_valid(self):
		assignment = {'first': 'foo', 'last': 'bar', 'age': 13}
		op = (Insert(self.column_family)
			.values(**assignment)
		)
		cql, args = op.statement()
		self.assertEquals(cql, self.get_query(assignment))
		self.assertEquals(args, assignment.values())		

	def test_options(self):
		assignment = {'name': 'foo'}
		using = Using(ttl=10800)
		op = (Insert(self.column_family)
			.values(**assignment)
			.using(**using.options)
		)
		cql, args = op.statement()
		query = self.get_query(assignment)
		self.assertEquals(cql, '{} {}'.format(query, using.cql))
		self.assertEquals(args, assignment.values() + using.values)

	def test_if_not_exists(self):
		assignment = {'name': 'foo'}
		op = (Insert(self.column_family)
			.values(**assignment)
			.if_not_exists()
		)
		cql, args = op.statement()
		query = self.get_query(assignment)
		self.assertEquals(cql, '{} IF NOT EXISTS'.format(query))
		self.assertEquals(args, assignment.values())

class TestUpdate(TestCase):

	def setUp(self):
		self.column_family = 'test_column_family'

	def get_query(self, assignment, condition, using=None):
		query = 'UPDATE {}'.format(self.column_family)
		if using:
			query = '{} {}'.format(query, using.cql)
		assignments = Assignments()
		assignments.add(assignment)
		where = Where(condition)
		return '{} SET {} WHERE {}'.format(query, assignments.cql, where.cql)

	def test_no_assignment(self):
		op = (Update(self.column_family)
			.where(eq('name', 'foo'))
		)
		self.assertRaises(ValidationError, op.statement)

	def test_no_condition(self):
		op = (Update(self.column_family)
			.set(name='foo')
		)
		self.assertRaises(ValidationError, op.statement)

	def test_valid(self):
		assignment = Set(first='foo')
		condition = eq('last', 'bar')
		op = (Update(self.column_family)
			.set(**assignment.kwargs)
			.where(condition)
		)
		cql, args = op.statement()
		self.assertEquals(cql, self.get_query(assignment, condition))
		self.assertEquals(args, assignment.values + condition.values)

	def test_options(self):
		assignment = Set(first='foo')
		condition = eq('last', 'bar')
		using = Using(ttl=10800)
		op = (Update(self.column_family)
			.using(**using.options)
			.set(**assignment.kwargs)
			.where(condition)
		)
		cql, args = op.statement()
		self.assertEquals(cql, self.get_query(assignment, condition, using))
		self.assertEquals(args, using.values + assignment.values + condition.values)

class TestSelect(TestCase):

	def setUp(self):
		self.column_family = 'test_column_family'

	def get_query(self, selection, condition=None):
		query = 'SELECT {} FROM {}'.format(selection.cql, self.column_family)
		if condition:
			where = Where(condition)
			query = '{} WHERE {}'.format(query, where.cql)
		return query

	def test_no_selection(self):
		op = Select(self.column_family)
		self.assertRaises(ValidationError, op.statement)

	def test_selection(self):
		selection = Columns('first', 'last')
		op = (Select(self.column_family)
			.columns(*selection.args)
		)
		cql, args = op.statement()
		self.assertEquals(cql, self.get_query(selection))
		self.assertEquals(args, selection.values)

	def test_condition(self):
		selection = Columns('first', 'last')
		condition = eq('name', 'foo')
		op = (Select(self.column_family)
			.columns(*selection.args)
			.where(condition)
		)
		cql, args = op.statement()
		self.assertEquals(cql, self.get_query(selection, condition))
		self.assertEquals(args, selection.values + condition.values)

	def test_limit(self):
		selection = Columns('first', 'last')
		limit = Limit(5)
		op = (Select(self.column_family)
			.columns(*selection.args)
			.limit(limit.value)
		)
		cql, args = op.statement()
		self.assertEquals(cql, '{} {}'.format(self.get_query(selection), limit.cql))
		self.assertEquals(args, selection.values + limit.values)

class TestDelete(TestCase):

	def setUp(self):
		self.column_family = 'test_column_family'

	def get_query(self, condition, selection=None):
		query = 'DELETE'
		if selection:
			query = '{} {}'.format(query, selection.cql)
		return '{} FROM {} WHERE {}'.format(query, self.column_family, condition.cql)

	def test_no_condition(self):
		op = Delete(self.column_family)
		self.assertRaises(ValidationError, op.statement)

	def test_no_selection(self):
		condition = eq('name', 'foo')
		op = (Delete(self.column_family)
			.where(condition)
		)
		cql, args = op.statement()
		self.assertEquals(cql, self.get_query(condition))
		self.assertEquals(args, condition.values)

	def test_selection(self):
		condition = eq('name', 'foo')
		selection = Columns('first', 'last')
		op = (Delete(self.column_family)
			.columns(*selection.args)
			.where(condition)
		)
		cql, args = op.statement()
		self.assertEquals(cql, self.get_query(condition, selection))
		self.assertEquals(args, condition.values + selection.values)

class TestTruncate(TestCase):

	def setUp(self):
		self.column_family = 'test_column_family'

	def test_valid(self):
		op = Truncate(self.column_family)
		cql, args = op.statement()
		self.assertEquals(cql, 'TRUNCATE {}'.format(self.column_family))
		self.assertEquals(args, [])

if __name__ == '__main__':
	unittest.main()
