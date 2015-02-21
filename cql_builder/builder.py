from cql_builder.statement import Insert, Update, Select, Delete, Truncate

class QueryBuilder(object):

	@staticmethod
	def insert_into(column_family, keyspace=None):
		return Insert(column_family, keyspace)

	@staticmethod
	def update(column_family, keyspace=None):
		return Update(column_family, keyspace)

	@staticmethod
	def select_from(column_family, keyspace=None):
		return Select(column_family, keyspace)

	@staticmethod
	def delete_from(column_family, keyspace=None):
		return Delete(column_family, keyspace)

	@staticmethod
	def truncate(column_family, keyspace=None):
		return Truncate(column_family, keyspace)
