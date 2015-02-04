from cql_builder.statement import Insert, Update, Select

class QueryBuilder(object):

	@staticmethod
	def insert_into(keyspace, column_family):
		return Insert(keyspace, column_family)

	@staticmethod
	def update(keyspace, column_family):
		return Update(keyspace, column_family)

	@staticmethod
	def select_from(keyspace, column_family):
		return Select(keyspace, column_family)
