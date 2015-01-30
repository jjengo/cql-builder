from cql_builder.statement import Insert, Update

class QueryBuilder(object):

	@staticmethod
	def insert_into(keyspace, column_family):
		return Insert(keyspace, column_family)

	@staticmethod
	def update(keyspace, column_family):
		return Update(keyspace, column_family)
